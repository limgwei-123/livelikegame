import uuid
from typing import Protocol
from app.workflows.redemption_workflow.schemas import RedeemRewardResponse

class RedemptionWorkflowServiceInterface(Protocol):

    def redemption_workflow(self, reward_id: int, user_id: uuid.UUID) -> RedeemRewardResponse:
        ...
