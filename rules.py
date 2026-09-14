from claim_model import Rule, EvaluationResult
rejection_rules={
    "R01": Rule(
        cause="Example 1",
        action="Example of corrective Action1",
        grievance_path="Example grievance path 1",
        deadline_days= 30    
    ),
    "R02": Rule(
        cause="Example 2",
        action="Example of corrective Action2",
        grievance_path="Example grievance path 2",
        deadline_days= 20    
    ),
    "R03": Rule(
        cause="Example 3",
        action="Example of corrective Action3",
        grievance_path="Example grievance path 3",
        deadline_days= 25   
    )
        
    
}


def get_rules(rejection_code):
    lata=rejection_rules.get(rejection_code)
    return lata


   
def evaluate_claim(rejection_code):
    rule=get_rules(rejection_code)
    if not is_rule_valid(rule):
        return EvaluationResult(
            valid=False,
            rule=None
        )
    return EvaluationResult(
        valid=True,
        rule=rule
    )

def is_rule_valid(rule):##if everything is present return true , if something is miss return false
    if rule is None:
        return False

    if not rule.cause:
        return False

    if not rule.action:
        return False

    if not rule.grievance_path:
        return False

    if rule.deadline_days<0:
        return False

    return True