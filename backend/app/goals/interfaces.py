from typing import Protocol
import uuid
from app.goals.models import Goal
from app.goals.schemas import CreateGoalRequest, UpdateGoalRequest

class GoalServiceInterface(Protocol):
  def create_goal(self, user_id: uuid.UUID, payload: CreateGoalRequest) -> Goal:
    ...

  def list_goals(self, user_id: uuid.UUID) -> list[Goal]:
    ...

  def get_goal_by_id(self, goal_id: int, user_id: uuid.UUID) -> Goal:
    ...

  def update_goal(self, goal_id: int, user_id: uuid.UUID, data: UpdateGoalRequest) -> Goal:
    ...

  def delete_goal(self, goal_id: int, user_id: uuid.UUID) -> None:
    ...
