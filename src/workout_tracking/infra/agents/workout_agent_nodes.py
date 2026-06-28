from datetime import datetime
from uuid import UUID

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from workout_tracking.infra.agents.prompts import WORKOUT_SYSTEM_PROMPT
from langchain_google_genai import ChatGoogleGenerativeAI

from workout_tracking.infra.agents.workout_agent_types import (
    ExerciseData,
    PreparedWorkoutData,
    WorkoutExtraction,
    WorkoutState,
)
from workout_tracking.infra.repositories.exercise_repository import ExerciseRepository
from workout_tracking.infra.repositories.user_exercise_repository import (
    UserExerciseRepository,
)


class WorkoutAgentNodes:
    def __init__(
        self,
        llm: ChatGoogleGenerativeAI,
        exercise_repository: ExerciseRepository,
        user_exercise_repository: UserExerciseRepository,
    ):
        self._llm = llm
        self._exercise_repository = exercise_repository
        self._user_exercise_repository = user_exercise_repository

    async def prepare_workout_node(
        self, state: WorkoutState, config: RunnableConfig
    ) -> WorkoutState:
        last_message = state["messages"][-1]
        user_id = config["configurable"]["actor_id"]
        workout_date = self._extract_date(last_message.content)

        all_exercises = await self._exercise_repository.get_all_exercises()
        exercise_list = "\n".join(
            [
                f"- {ex.name}: {ex.description or 'No description'}"
                for ex in all_exercises
            ]
        )

        prompt = f"""
        Available exercises:
        {exercise_list}

        User message: {last_message.content}
        User ID: {user_id}
        Workout date: {workout_date}
        """

        structured_llm = self._llm.with_structured_output(WorkoutExtraction)

        extracted_data = await structured_llm.ainvoke([
            SystemMessage(content=WORKOUT_SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ])

        prepared_workout = PreparedWorkoutData(
            user_id=user_id if isinstance(user_id, UUID) else UUID(user_id),
            exercises=[
                ExerciseData(
                    exercise_name=ex.name,
                    sets=ex.sets,
                    reps=ex.reps,
                    weight=ex.weight
                ) for ex in extracted_data.exercises
            ],
            workout_date=workout_date,
        )

        state["prepared_workout"] = prepared_workout
        state["confirmation_status"] = "pending"
        state["messages"].append(
            AIMessage(
                content=f"Prepared workout data:\n{self._format_workout_summary(prepared_workout)}\n\nPlease confirm or reject."
            )
        )

        return state

    async def confirm_workout_node(
        self, state: WorkoutState, config: RunnableConfig
    ) -> WorkoutState:
        last_message = state["messages"][-1]
        confirmed = "confirm" in last_message.content.lower()

        if not confirmed:
            state["prepared_workout"] = None
            state["confirmation_status"] = "rejected"
            state["messages"].append(
                AIMessage(
                    content="Workout data discarded. You can prepare new workout data."
                )
            )
            return state

        prepared_workout = state["prepared_workout"]
        results = []

        for exercise_data in prepared_workout.exercises:
            exercise_id = await self._find_exercise_id(exercise_data.exercise_name)
            if exercise_id:
                from workout_tracking.infra.repositories.user_exercise_repository_types import (
                    CreateUserExerciseInput,
                )

                user_exercise_input = CreateUserExerciseInput(
                    user_id=prepared_workout.user_id,
                    exercise_id=exercise_id,
                    sets=exercise_data.sets,
                    reps=exercise_data.reps,
                    weight=exercise_data.weight,
                    date=prepared_workout.workout_date,
                    job_id=config["configurable"]["thread_id"],
                )

                await self._user_exercise_repository.create_user_exercise(
                    user_exercise_input
                )
                results.append(f"Saved: {exercise_data.exercise_name}")

        state["prepared_workout"] = None
        state["confirmation_status"] = "confirmed"
        state["messages"].append(
            AIMessage(content="Workout saved successfully!\n" + "\n".join(results))
        )

        return state

    def _extract_date(self, message: str):
        return datetime.now().date()

    def _format_workout_summary(self, workout: PreparedWorkoutData) -> str:
        summary = f"User ID: {workout.user_id}\n"
        summary += f"Date: {workout.workout_date}\n"
        summary += "Exercises:\n"
        for ex in workout.exercises:
            summary += f"- {ex.exercise_name}: {ex.sets} sets x {ex.reps} reps @ {ex.weight}kg\n"
        return summary

    async def _find_exercise_id(self, exercise_name: str) -> UUID | None:
        all_exercises = await self._exercise_repository.get_all_exercises()
        for ex in all_exercises:
            if exercise_name.lower() in ex.name.lower():
                return ex.id
        return None
