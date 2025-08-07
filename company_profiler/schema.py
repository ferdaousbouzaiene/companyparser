from dataclasses import dataclass, asdict, field


@dataclass
class CompanyProfile:
    company_name: str = "unknown"
    industry: str = "unknown"
    founding_date: str = "unknown"
    business_model: str = "unknown"
    target_customers: str = "unknown"
    key_value_proposition: str = "unknown"
    geographical_focus: str = "unknown"
    funding_stage: str = "unknown"


    def to_dict(self):
        return asdict(self)
