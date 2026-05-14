import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger=logging.getLogger("airflow.task")
def transform_data():
    try:
        logger.info("Rading data from reddit_posts.csv")
        df=pd.read_csv("reddit_posts.csv")
        df.dropna(inplace=True)
        logger.info(f"rows after dropping null values: {len(df)}")
        df.drop_duplicates(inplace=True)
        logger.info(f"rows after dropping duplicates: {len(df)}")
        df["title"]=df["title"].str.strip()
        df["author"]=df["author"].str.strip()
        df["subreddit"]=df["subreddit"].str.strip()
        logger.info("Transformed data successfully")
        df.to_csv("transformed_reddit_posts.csv", index=False)


    except Exception as e:
        logger.error(f"Error transforming data: {e}")
        raise
if __name__ == "__main__":
    transform_data()