import pandas as pd
import requests
import logging
import random
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger=logging.getLogger("airflow.task")
SUBREDDITS = [
        "MachineLearning",
        "OpenAI",
        "artificial"
]

HEADERS = {
        "User-Agent": "python:reddit.pipeline:v1.0 (by /u/soumyadeep)"
    }
# Function to fetch Reddit data and return a list of posts
def fetch_reddit_data():
  all_posts=[]
  logger.info("Starting Reddit data ingestion")
  for subreddit in SUBREDDITS:
     url=f"https://www.reddit.com/r/{subreddit}/.json?limit={random.randint(5, 25)}"
     try:
        response=requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data=response.json()
        posts=data["data"]["children"]
        for post  in posts:
            all_posts.append({
                    "subreddit": subreddit,
                    "title": post["data"].get("title"),
                    "author": post["data"].get("author"),
                    "ups": post["data"].get("ups"),
                    "downs": post["data"].get("downs"),
                    "created_utc": post["data"].get("created_utc"),
                })
        logger.info(f"Fetched {len(posts)} posts from r/{subreddit}")     
     except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from {subreddit}: {e}")
  return all_posts
# Function to save the list of posts to a CSV file
def save_to_csv(posts):
    df=pd.DataFrame(posts)
    try:
     df.to_csv("reddit_posts.csv", index=False)
     logger.info("Saved Reddit data to reddit_posts.csv")
    except Exception as e:
        logger.error(f"Error saving data to CSV: {e}")
        raise      
def fetch_and_save():
    reddit_posts=fetch_reddit_data()
    save_to_csv(reddit_posts)
if __name__ == "__main__":
    fetch_and_save()