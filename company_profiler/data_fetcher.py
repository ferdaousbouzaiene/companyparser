import wikipediaapi
def fetch_company_summary(company_name: str) -> str:

    """
    Fetch:      the summary of a company from Wikipedia
    Args:       company_name (str): The name of the company
    Returns:    str: A summary text from the company's Wikipedia page
    Raises:     ValueError: If the Wikipedia page doesn't exist
    """

    wiki = wikipediaapi.Wikipedia(
        language="en",
        user_agent="LLMCompanyProfiler/1.0 (ferdaous.bouzaine@gmail.com)"
    )
    
    page = wiki.page(company_name)

    if not page.exists():
        raise ValueError(f"No Wikipedia page found for '{company_name}'")
    
    summary = page.summary.strip()

    if not summary:
        raise ValueError(f"Page for '{company_name}' exists but has no summary.")

    return summary
