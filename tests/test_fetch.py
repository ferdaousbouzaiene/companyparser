from company_profiler.data_fetcher import fetch_company_summary

def test_fetch_summary():
    # Try different variations
    test_names = ["Pinterest (company)", "Pinterest Inc", "Pinterest"]
    
    for name in test_names:
        try:
            summary = fetch_company_summary(name)
            print(f"✅ {name}: {len(summary)} chars - {repr(summary[:100])}")
            if len(summary) > 50:
                break
        except ValueError as e:
            print(f"❌ {name}: {e}")

if __name__ == "__main__":
    test_fetch_summary()
