from claim_model import Rule
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
    if rule is None:
        return {
            "valid": False,
            "rule": None
        }
    return {
        "valid": True,
        "rule": rule
    }

