import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import re
load_dotenv()  # Loads your .env file for OPENAI_API_KEY

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))





def extract_company_profile(summary: str) -> dict:
    """
    Use OpenAI's LLM to extract structured company info from a summary.
    
    Args:
        summary (str): Raw company description (e.g., from Wikipedia)
    
    Returns:
        dict: Structured company profile
    """

    system_prompt = "You're an expert business analyst. Based on company summaries, extract or infer the following fields...."

    user_prompt = f"""
Given the following company description, extract these fields:

- company_name
- industry
- founding_date
- business_model (e.g., B2B SaaS, marketplace, etc.)
- target_customers (e.g., enterprise, SMBs, developers)
- key_value_proposition (1 to 2 sentences)
- geographical_focus (e.g., US, Europe, Global)
- funding_stage (e.g., Seed, Series A, Public)

If any field is unknown, return "unknown".

Company Description:
\"\"\"
{summary}
\"\"\"

Return your response as a JSON object.
"""

    response = client.chat.completions.create(model="gpt-3.5-turbo",  
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0)

    content = response.choices[0].message.content.strip()

    # Remove common markdown wrapping
    content = re.sub(r'^```(?:json)?\s*|\s*```$', '', content, flags=re.MULTILINE)

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ Failed to parse JSON from LLM response: {e}\nContent: {content}")