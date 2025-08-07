import sys
import json

from company_profiler.data_fetcher import fetch_company_summary
from company_profiler.llm_parser import extract_company_profile
from company_profiler.schema import CompanyProfile


def main():
    if len(sys.argv) != 2:
        print("Usage: python profile_builder.py '<Company Name>'")
        sys.exit(1)

    company_name = sys.argv[1]

    try:
        print(f"🔍 Fetching summary for: {company_name}")
        summary = fetch_company_summary(company_name)
        print("\n📄 Wikipedia Summary:\n")
        print(summary)


        print("🤖 Extracting structured profile with LLM...")
        raw_profile = extract_company_profile(summary)

        # Convert to dataclass
        profile = CompanyProfile(**raw_profile)

        print("\n✅ Company Profile:\n")
        print(json.dumps(profile.to_dict(), indent=2))

        filename = f"{company_name.lower().replace(' ', '_')}_profile.json"
        with open(filename, "w") as f:
            json.dump(profile.to_dict(), f, indent=2)

        print(f"\n💾 Saved to: {filename}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
