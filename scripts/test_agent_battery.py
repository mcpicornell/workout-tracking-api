import asyncio
import os
from uuid import uuid4
from datetime import date
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

from workout_tracking.infra.agents.workout_agent import DefaultWorkoutAgent
from workout_tracking.infra.agents.workout_agent_types import LLMSettings, ProcessWorkoutMessageInput
from workout_tracking.infra.repositories.exercise_repository import DefaultExerciseRepository
from workout_tracking.infra.repositories.user_exercise_repository import DefaultUserExerciseRepository
from workout_tracking.infra.db.models import Base, Exercise

load_dotenv()

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

async def setup_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSession(engine) as session:
        exercises = [
            Exercise(name="Press Banca Inclinado", description="Chest"),
            Exercise(name="Sentadillas", description="Legs"),
            Exercise(name="Press Militar", description="Shoulders"),
            Exercise(name="Peso Muerto", description="Back/Legs"),
        ]
        session.add_all(exercises)
        await session.commit()

async def main():
    engine = create_async_engine(DATABASE_URL)
    await setup_db(engine)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    settings = LLMSettings(
        name=os.getenv("LLM_MODEL", "gemini-1.5-pro"),
        api_key=os.getenv("GOOGLE_API_KEY")
    )

    if not settings.api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return

    async with async_session() as session:
        exercise_repo = DefaultExerciseRepository(session)
        user_exercise_repo = DefaultUserExerciseRepository(session)
        
        agent = DefaultWorkoutAgent(
            exercise_repository=exercise_repo,
            user_exercise_repository=user_exercise_repo,
            checkpointer=MemorySaver(),
            settings=settings,
        )

        test_cases = [
            "Hoy he hecho press banca inclinado, 3 series de 10 repeticiones con 50, 60 y 70kg respectivamente",
            "I did 3x12 squats at 100kg",
            "Hice 3 series de 8 de press militar con 40kg",
            "Did some deadlifts 5 reps 120kg",
        ]

        user_id = uuid4()
        
        for i, text in enumerate(test_cases):
            job_id = uuid4()
            print(f"\n--- Test Case {i+1}: {text} ---")
            
            input_data = ProcessWorkoutMessageInput(
                user_id=user_id,
                job_id=job_id,
                message=text,
                workout_date=date.today()
            )
            
            try:
                result = await agent.process_workout_message(input_data)
                print(f"Agent Response:\n{result.content}")
                
                confirmation = await agent.confirm_workout(confirmed=True, job_id=job_id, user_id=user_id)
                print(f"Confirmation Response:\n{confirmation}")
                
            except Exception as e:
                print(f"Error processing test case: {e}")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
