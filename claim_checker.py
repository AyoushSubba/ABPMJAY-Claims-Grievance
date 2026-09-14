from claim_model import Claim,Rule,EvaluationResult
from rules import rejection_rules,evaluate_claim

claim=Claim(
  claim_id="C1024",
  rejection_code="R022",
  status="REJECTED"
)
if claim.status=="REJECTED":
    result=evaluate_claim(claim.rejection_code)
    if not result.valid:
      print("There is no valid rule!!")
    else:
      rule=result.rule
      print("the reason is: ",rule.cause)
      print("The action that can be taken is:", rule.action)
      print("Grievance path:", rule.grievance_path)
      print("Deadline Delays:",rule.deadline_days)

else:
    print("I think it is accepted!!")