from pydantic import BaseModel, Field

class Transfer(BaseModel):
    from_account_id: int = Field(..., description="ID of the sender's account")
    to_account_id: int = Field(..., description="ID of the receiver's account")
    amount: float = Field(..., description="Amount to transfer")
