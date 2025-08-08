# LLM Company Profiler

A lightweight command-line tool that generates structured company profiles using publicly available data and a large language model.

You give it a company name and it returns a clean json-formatted-profile including industry, business model, target customers, and more.

---

##  What It Does Exactly

- Fetches a company's summary from Wikipedia
- Uses a language model (GPT3.5T) to extract or infer key business attributes
- Outputs the result as JSON and saves it to a file

---

## Fields Extracted

- `company_name`
- `industry`
- `founding_date`
- `business_model`
- `target_customers`
- `key_value_proposition`
- `geographical_focus`
- `funding_stage`

---

## Prerequisites

Before you begin, make sure you have:

- **Python 3.9+** installed  
  (Project tested on Python 3.11 — may work on older versions but not guaranteed)
- **pip** (Python package manager) available in your environment
- An **OpenAI API key** (for GPT integration)
- Internet connection (to fetch data from Wikipedia and call the OpenAI API)


---

## Setup and Usage Instructions

1. Clone the repo:

   ```bash
   git clone https://github.com/ferdaousbouzaiene/companyparser.git
   cd companyparser

2. Create a virtual environment

     ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Mac/Linux
    venv\Scripts\activate     # On Windows


3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Add openAi key to .env
    ```bash
    echo "OPENAI_API_KEY=your-api-key-here" > .env

5. From project root, run: 
    ```bash
    PYTHONPATH=. python3 company_profiler/profile_builder.py "SoundClouds"


## Assumptions

Company summaries are pulled from Wikipedia

If exact matches aren’t found, the model attempts to infer based on context

Missing data is labeled as "unknown" by default

## Improvements

Batch input for multiple companies

Crunchbase/LinkedIn integration

Web app interface

Caching for repeated queries

## Troubleshooting

- **ModuleNotFoundError**: Make sure you're running from project root with `PYTHONPATH=.`
- **Wikipedia page not found**: Try variations like "Company Name Inc" or "Company Name (company)"
- **API errors**: Check your OpenAI API key and account credits