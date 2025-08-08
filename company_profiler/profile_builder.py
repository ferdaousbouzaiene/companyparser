# company_profiler/profile_builder.py
import argparse
import json
import logging
from dataclasses import asdict, fields

from company_profiler.data_fetcher import fetch_company_summary
from company_profiler.llm_parser import extract_company_profile
from company_profiler.schema import CompanyProfile

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

DEFAULTS = {
    "company_name": "Not available",
    "industry": "Unknown industry",
    "founding_date": "Unknown",
    "business_model": "Unknown",
    "target_customers": "Not specified",
    "key_value_proposition": "No description available.",
    "geographical_focus": "Not specified",
    "funding_stage": "Unknown"
}

def normalize_profile(raw: dict, user_provided_name: str) -> dict:
    result = {}
    for f in fields(CompanyProfile):
        if f.name == "company_name":
            # Use the company name from CLI args as most reliable source
            val = user_provided_name.title()
            val = user_provided_name
        else:
            val = str(raw.get(f.name, "") or "").strip()
            if not val or val.lower() == "unknown":
                val = DEFAULTS[f.name]
        result[f.name] = val
    return result



def main():
    parser = argparse.ArgumentParser(description="Generate a structured company profile.")
    parser.add_argument("company", help="Company name, e.g., 'Datadog'")
    args = parser.parse_args()

    try:
        logging.info("🔍 Fetching summary for: %s", args.company)
        summary = fetch_company_summary(args.company)

        logging.info("🤖 Extracting structured profile with LLM…")
        raw_profile = extract_company_profile(summary)
        cleaned = normalize_profile(raw_profile, args.company)
        profile = CompanyProfile(**cleaned)
        serialized = json.dumps(asdict(profile), indent=2)

        filename = args.company.lower().replace(" ", "_") + "_profile.json"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(serialized)

        logging.info("💾 Saved to: %s", filename)
        logging.info("\n%s", serialized)

    except Exception as e:
        logging.error("❌ Error: %s", e)

if __name__ == "__main__":
    main()
