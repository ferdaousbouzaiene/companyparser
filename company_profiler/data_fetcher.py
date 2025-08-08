#### Wikipedia search + summary

import logging
import wikipedia

wikipedia.set_lang("en")

try:
    wikipedia.set_user_agent("LLMCompanyProfiler/1.0 (ferdaous.bouzaine@gmail.com)")
except AttributeError:
    pass

def fetch_company_summary(company_name: str, min_chars: int = 80) -> str:
    """
    Fetch a company's summary from Wikipedia using search for better matching.
    Returns the first good summary found, or raises ValueError if none found.
    """
    logging.info("🔍 Searching Wikipedia for: %s", company_name)

    try:
        results = wikipedia.search(company_name)
    except Exception as e:
        raise ValueError(f"Wikipedia search failed: {e}")

    if not results:
        raise ValueError(f"No Wikipedia results for '{company_name}'")

    logging.info("Found candidates: %s", results[:3])

    for title in results:
        try:
            page = wikipedia.page(title, auto_suggest=False, preload=True)
            summary = (page.summary or "").strip()
            if len(summary) >= min_chars:
                logging.info("✅ Using page: %s", title)
                return summary
        except wikipedia.exceptions.DisambiguationError as e:
            logging.warning("Disambiguation for '%s': %s", title, e.options[:3])
        except wikipedia.exceptions.PageError:
            logging.warning("Page not found for '%s'", title)
        except Exception as e:
            logging.warning("Error fetching '%s': %s", title, e)

    raise ValueError(f"No suitable Wikipedia summary found for '{company_name}'")
