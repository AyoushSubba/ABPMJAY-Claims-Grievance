from pydantic import BaseModel
class Claim(BaseModel):
    claim_id:str
    rejection_code:str
    status:str

class Rule(BaseModel):
    cause:str
    action:str
    grievance_path:str
    deadline_days:int
class EvaluationResult(BaseModel):
    valid: bool
    rule: Rule | None