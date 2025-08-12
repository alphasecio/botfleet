import logging
import requests
from shared.logging_utils import setup_logging
from shared.email_utils import send_email

setup_logging()

HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty&orderBy=\"$priority\"&limitToFirst=50"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"

def fetch_top_stories(limit):
    try:
        response = requests.get(HN_TOP_STORIES_URL, timeout=10)
        response.raise_for_status()
        story_ids = response.json()
        
        stories = []
        for sid in story_ids[:limit]:
            item_response = requests.get(HN_ITEM_URL.format(id=sid), timeout=10)
            item_response.raise_for_status()
            story = item_response.json()
            if story and 'title' in story and 'url' in story:
                stories.append(story)
        return stories
    except Exception as e:
        logging.error(f"Error fetching top stories: {e}")
        return []

def main():
    stories = fetch_top_stories(limit=50)
    if not stories:
        logging.info("No stories fetched, skipping email.")
        return

    email_body_parts = []
    for i, story in enumerate(stories, start=1):
        email_body_parts.append(f"<p>{i}. {story['title']}<br>"
                                f"<a href='{story['url']}'>{story['url']}</a></p>")
    
    send_email("Hacker News Top Stories", "".join(email_body_parts))

if __name__ == "__main__":
    main()
