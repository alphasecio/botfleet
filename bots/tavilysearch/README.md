# 📰 tavilysearch

This bot searches for recent news using the [Tavily API](https://docs.tavily.com/) and sends the top results via email using the [Resend API](https://resend.com/docs).


### 🚀 Running the Bot Locally
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set the required environment variables (see table below).
4. Run the bot: `python bots/tavilysearch/main.py`


### 🚀 Deploying to Railway

Click the button below to deploy:

  [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new?referralCode=alphasec)

Then, on Railway:
1. Create an empty project and a new service using the `Deploy from GitHub repo` option.
2. Add a custom start command: `python -m bots.tavilysearch.main`.
3. Set the required environment variables in the `Variables` tab.
4. Set the `Cron Schedule` in the `Settings` tab and click Deploy.


### 🌐 Environment Variables

| Variable             | Required | Description                                           |
|----------------------|----------|-------------------------------------------------------|
| `TAVILY_URL`         |          | Tavily URL (default: `https://api.tavily.com/search`) |
| `TAVILY_API_KEY`     |    ✅    | Tavily API key                                        |
| `RESEND_URL`         |          | Resend URL (default: `https://api.resend.com/emails`) |
| `RESEND_API_KEY`     |    ✅    | Resend API key                                        |
| `EMAIL_FROM`         |    ✅    | Sender email address                                  |
| `EMAIL_TO`           |    ✅    | Recipient email address                               |
| `EMAIL_SUBJECT`      |          | Subject line for the email                            |
| `SEARCH_QUERY`       |    ✅    | Search keywords                                       |
| `SEARCH_TOPIC`       |          | Topic category (default: `news`)                      |
| `SEARCH_DEPTH`       |          | `basic` or `advanced` (default: `advanced`)           |
| `SEARCH_DAYS`        |          | Lookback window in days (default: `7`)                |
| `MAX_RESULTS`        |          | Max number of URLs to include (default: `10`)         |
| `INCLUDE_ANSWER`     |          | LLM summary `true` or `false` (default: `false`)      |


### ✉️ Sample Email Alert

> **News results for: "AI regulation"**
>
> Found 10 results:
> - `https://example.com/article1`  
> - `https://example.com/article2`  
> - ...
