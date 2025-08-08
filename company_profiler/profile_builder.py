import sys
import json
import logging
from company_profiler.data_fetcher import fetch_company_summary
from company_profiler.llm_parser import extract_company_profile
from company_profiler.schema import CompanyProfile

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python profile_builder.py '<Company Name>'")
        sys.exit(1)

    company_name = sys.argv[1]

    try:
        logger.info(f"🔍 Fetching summary for: {company_name}")
        summary = fetch_company_summary(company_name)
        logger.info("📄 Wikipedia summary fetched successfully")
        logger.debug(f"Summary content:\n{summary}")
        logger.info("🤖 Extracting structured profile with LLM...")
        raw_profile = extract_company_profile(summary)

        # Convert to dataclass
        profile = CompanyProfile(**raw_profile)
        logger.info("✅ Company profile generated successfully")
        logger.debug(json.dumps(profile.to_dict(), indent=2))

        filename = f"{company_name.lower().replace(' ', '_')}_profile.json"
        try:
            with open(filename, "w") as f:
                json.dump(profile.to_dict(), f, indent=2)
            logger.info(f"💾 Successfully saved to: {filename}")
        except IOError as e:
            logger.error(f"❌ Failed to save file: {e}")
            raise  # Re-raise to let outer exception handler deal with it

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
