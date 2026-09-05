import uuid
from typing import Protocol
from app.workflows.task_workflow.schemas import (
    ConfirmAiPlanRequest,
    CreateTaskWithScheduleRequest,
    GoalTaskSchduleResponse,
    TaskWithScheduleResponse,
)

class TaskWorkflowServiceInterface(Protocol):
  def create_task_with_schedule(
      self,
      goal_id: int,
      user_id: uuid.UUID,
      payload: CreateTaskWithScheduleRequest
  ) -> TaskWithScheduleResponse:
    ...

  def create_from_ai_plan(self, user_id: uuid.UUID, payload: ConfirmAiPlanRequest) -> GoalTaskSchduleResponse:
    ...
