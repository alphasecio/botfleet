import logging
import requests
from shared.config import get_env
from shared.logging_utils import setup_logging
from shared.email_utils import send_email

setup_logging()

TAVILY_URL = get_env("TAVILY_URL", "https://api.tavily.com/search")
TAVILY_API_KEY = get_env("TAVILY_API_KEY", required=True)
SEARCH_QUERY = get_env("SEARCH_QUERY", required=True)
SEARCH_TOPIC = get_env("SEARCH_TOPIC", "news")
SEARCH_DEPTH = get_env("SEARCH_DEPTH", "advanced")
SEARCH_DAYS = int(get_env("SEARCH_DAYS", 7))
INCLUDE_ANSWER = get_env("INCLUDE_ANSWER", "false")
MAX_RESULTS = int(get_env("MAX_RESULTS", 10))
EMAIL_SUBJECT = get_env("EMAIL_SUBJECT", f"Tavily Search Results: {SEARCH_QUERY}")

def search_and_extract_urls():
    try:
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": SEARCH_QUERY,
            "search_depth": SEARCH_DEPTH,
            "topic": SEARCH_TOPIC,
            "days": SEARCH_DAYS,
            "max_results": MAX_RESULTS,
            "include_answer": INCLUDE_ANSWER,
        }
        logging.info(f"Sending request to Tavily API with payload: {payload}")
        response = requests.post(TAVILY_URL, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        return [r.get("url") for r in data.get("results", []) if r.get("url")]
    except Exception as e:
        logging.error(f"Tavily API error: {e}")
        return []

def main():
    urls = search_and_extract_urls()
    logging.info(f"Found {len(urls)} results")
    if not urls:
        logging.info("No results found, skipping email.")
        return

    html_content = [
        f"<h2>News results for: \"{SEARCH_QUERY}\"</h2>",
        f"<p>Found {len(urls)} results:</p>",
        "<ul>",
    ]
    html_content.extend([f"<li><a href='{url}'>{url}</a></li>" for url in urls])
    html_content.append("</ul>")

    send_email(EMAIL_SUBJECT, "".join(html_content))

if __name__ == "__main__":
    main()
