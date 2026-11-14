# Top FDE Roles Hiring Tracker

A fast, zero-dependency CLI tool to track and display the top **Forward Deployed Engineer (FDE)** and **Forward Deployed Software Engineer (FDSE)** roles actively hiring this month across top AI labs, infrastructure pioneers, and enterprise tech.

---

## What is a Forward Deployed Engineer (FDE)?

Pioneered by Palantir and now widely adopted across frontier AI companies (OpenAI, Anthropic, Scale AI) and enterprise infrastructure giants, **Forward Deployed Engineers** are hybrid systems engineers who embed directly with high-value enterprise customers. They build production-grade architectures, write custom integration code on client infrastructure, and feed enterprise requirements back to core platform teams.

---

## Usage

Run directly with standard Python 3 (no `pip install` required):

```bash
# View all top active FDE roles
python3 app.py
# or directly:
./app.py
```

### Filtering & Search Options

```bash
# Filter for remote-friendly roles only
python3 app.py --remote

# Search by keyword, tech stack, or city
python3 app.py --query "Python"
python3 app.py --query "San Francisco"

# Filter by company name
python3 app.py --company "OpenAI"

# Deep-dive into a specific role's tech stack and requirements
python3 app.py --detail 1

# Output as JSON (great for jq or downstream scripts)
python3 app.py --json

# Export to Markdown or CSV
python3 app.py --export roles.md
python3 app.py --export roles.csv
```

---

## Tracked Companies This Month

- **OpenAI** – Applied AI / Enterprise Agentic Pipelines
- **Anthropic** – Enterprise Deployment / Claude API
- **Palantir Technologies** – Commercial & AIP Forward Deployed Software Engineer
- **Scale AI** – GenAI Platform & Model Evaluation
- **Databricks** – Mosaic AI & Lakehouse Field Engineering
- **Vercel** – Enterprise Architecture & Edge AI
- **MongoDB** – Atlas Vector Search & RAG Architectures
- **Hightouch** – Data Activation & Reverse ETL
- **bp** – AI & Quantitative Energy Trading
- **Tesla** – Factory Automation & Industrial IoT
