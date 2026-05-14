from sqlalchemy import create_engine
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("airflow.task")

def create_db_connection():
    try:
        return create_engine("postgresql+psycopg2://postgres:12345@localhost:5432/reddit_db", connect_args={"connect_timeout":10 })
        logger.info("Database connection created successfully")

    
    except Exception as e:
        logger.error(f"Error creating database connection: {e}")
        raise
def load_data_to_db():
    try:
        engine = create_db_connection()
        try:
          df = pd.read_csv("transformed_reddit_posts.csv")
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            raise

        
        with engine.connect() as conn:
           
            df.to_sql(
                "reddit_posts",
                con=conn, 
                if_exists="replace",
                index=False
            )


        logger.info("Data loaded successfully")

    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise
if __name__ == "__main__":
    load_data_to_db()