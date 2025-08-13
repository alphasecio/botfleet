import logging
import requests
from shared.logging_utils import setup_logging
from shared.email_utils import send_email

setup_logging()

# Your Reddit app credentials (from https://www.reddit.com/prefs/apps)
CLIENT_ID = get_env("CLIENT_ID")
CLIENT_SECRET = get_env("CLIENT_SECRET")
USER_AGENT = get_env("USER_AGENT", "netsec-digest-bot/0.1")
SUBREDDIT = get_env("SUBREDDIT", "netsec")
EMAIL_SUBJECT = get_env("EMAIL_SUBJECT", f"Reddit /r/{SUBREDDIT} Top Stories")

OAUTH_URL = "https://www.reddit.com/api/v1/access_token"
BASE_URL = f"https://oauth.reddit.com/r/{SUBREDDIT}/new"

def fetch_latest_posts(limit):
    try:
        # Step 1: Get OAuth token
        auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
        data = {"grant_type": "client_credentials"}
        headers = {"User-Agent": USER_AGENT}

        logging.info("Requesting Reddit OAuth token...")
        token_response = requests.post(OAUTH_URL, auth=auth, data=data, headers=headers)
        token_response.raise_for_status()
        access_token = token_response.json()["access_token"]

        # Step 2: Use token to fetch subreddit posts
        headers["Authorization"] = f"bearer {access_token}"
        logging.info(f"Fetching latest {limit} posts from r/{SUBREDDIT}...")
        response = requests.get(BASE_URL, headers=headers, params={"limit": limit})
        response.raise_for_status()

        # Step 3: Parse posts
        posts = response.json()["data"]["children"]
        return posts
    except Exception as e:
        print(f"Error fetching latest posts: {e}")
        return []

def main():
    posts = fetch_latest_posts(limit=25)
    if not posts:
        logging.info("No posts fetched, skipping email.")
        return

    html_parts = [f"<h3>Latest posts from r/{SUBREDDIT}</h3>", "<ul>"]
    for post in posts:
        title = post["data"]["title"]
        url = "https://www.reddit.com" + post["data"]["permalink"]
        html_parts.append(f"<li><a href='{url}'>{title}</a></li>")
    html_parts.append("</ul>")

    send_email(EMAIL_SUBJECT, "".join(html_parts))

if __name__ == "__main__":
    main()
