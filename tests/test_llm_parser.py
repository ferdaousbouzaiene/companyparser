from company_profiler.llm_parser import extract_company_profile
from company_profiler.data_fetcher import fetch_company_summary

def test_extract():
    summary = fetch_company_summary("Pinterest")
    profile = extract_company_profile(summary)

    print("✅ Extracted Company Profile:")
    for key, value in profile.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    test_extract()
