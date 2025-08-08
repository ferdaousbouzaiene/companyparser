#### OpenAI Prompt + JSON parsing

import os
import re
import json
import time
import openai
from dotenv import load_dotenv

load_dotenv()  # Loads .env file for OPENAI_API_KEY

def strip_markdown_code(text: str) -> str:
    """
    Remove markdown code fencing from LLM output
    """
    if text.startswith("```") and text.endswith("```"):
        lines = text.strip().splitlines()
        # Remove first and last lines (fencing)
        return "\n".join(lines[1:-1]).strip()
    return text.strip()



def extract_company_profile(summary: str) -> dict:
    """
    Use OpenAI's LLM to extract structured company info from a summary
    Args: summary (str): Raw company description (e.g. from Wikipedia)
    Returns: dict: Structured company profile
    """

    openai.api_key = os.getenv('OPEN_API_KEY')

    system_prompt = "You're an expert business analyst. Based on company summaries, extract or infer the following fields...."

    user_prompt = f"""
    You are given a company summary. Extract the following fields as a clean, well-formatted JSON object:

    - company_name
    - industry
    - founding_date (as YYYY or YYYY-MM-DD if available)
    - business_model (e.g., B2B SaaS, Marketplace, Ad-based platform)
    - target_customers (e.g., Enterprise, SMBs, Developers, General public)
    - key_value_proposition (1–2 sentences, clearly written)
    - geographical_focus (e.g., US, Europe, Global)
    - funding_stage (e.g., Seed, Series A, Series B, Public)

    Return:
    - Properly capitalized values (e.g., "B2B SaaS", not "b2b saas")
    - Best-guess values if not explicitly stated — avoid "unknown" if you can infer from context
    - A raw JSON object only (no markdown, no code fences, no explanations)

    Company Description:
    \"\"\"
    {summary}
    \"\"\"
    """


    response = openai.chat.completions.create(model="gpt-3.5-turbo",  
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0)

    content = response.choices[0].message.content.strip()
    content = strip_markdown_code(content)

    if content.startswith('"') and content.endswith('"'):
        content = json.loads(content)

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ Failed to parse JSON from LLM response:\n{content}")