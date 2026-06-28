from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from uuid import UUID

from workout_tracking.infra.agents.workout_agent_nodes import WorkoutAgentNodes
from workout_tracking.infra.agents.workout_agent_types import (
    LLMSettings,
    ProcessWorkoutMessageInput,
    ProcessWorkoutMessageOutput,
    WorkoutState,
)
from workout_tracking.infra.repositories.exercise_repository import ExerciseRepository
from workout_tracking.infra.repositories.user_exercise_repository import (
    UserExerciseRepository,
)


class WorkoutAgent:
    def __init__(
        self,
        exercise_repository: ExerciseRepository,
        user_exercise_repository: UserExerciseRepository,
        checkpointer: MemorySaver,
        settings: LLMSettings,
    ):
        self._llm = ChatGoogleGenerativeAI(
            model=settings.name,
            api_key=settings.api_key,
        )

        self._nodes = WorkoutAgentNodes(
            llm=self._llm,
            exercise_repository=exercise_repository,
            user_exercise_repository=user_exercise_repository,
        )

        self._graph = self._build_graph(checkpointer)

    async def process_workout_message(
        self, input: ProcessWorkoutMessageInput
    ) -> ProcessWorkoutMessageOutput:
        config = {
            "configurable": {
                "thread_id": input.job_id,
                "actor_id": input.user_id,
            }
        }

        initial_state: WorkoutState = {
            "messages": [HumanMessage(content=input.message)],
            "prepared_workout": None,
            "confirmation_status": None,
        }

        result = await self._graph.ainvoke(initial_state, config=config)
        return ProcessWorkoutMessageOutput(content=result["messages"][-1].content)

    async def confirm_workout(self, confirmed: bool, job_id: UUID, user_id: UUID) -> str:
        config = {
            "configurable": {
                "thread_id": job_id,
                "actor_id": user_id,
            }
        }
        message = f"Please {'confirm' if confirmed else 'reject'} the workout data."
        initial_state: WorkoutState = {
            "messages": [HumanMessage(content=message)],
            "prepared_workout": None,
            "confirmation_status": None,
        }

        result = await self._graph.ainvoke(initial_state, config=config)
        return result["messages"][-1].content

    def _build_graph(self, checkpointer: MemorySaver):
        workflow = StateGraph(WorkoutState, checkpointer=checkpointer)

        workflow.add_node("prepare_workout", self._nodes.prepare_workout_node)
        workflow.add_node("confirm_workout", self._nodes.confirm_workout_node)

        workflow.set_entry_point("prepare_workout")

        def should_confirm(state: WorkoutState) -> str:
            if state.get("confirmation_status") == "pending":
                return "confirm_workout"
            return END

        workflow.add_conditional_edges(
            "prepare_workout",
            should_confirm,
            {"confirm_workout": "confirm_workout", END: END},
        )

        workflow.add_edge("confirm_workout", END)

        return workflow.compile()
