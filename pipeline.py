import logging
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError
import os


def main():
    logger = logging.getLogger("main")
    logger.setLevel(logging.INFO)
    # Add a log handler to the logger
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info("Starting the pipeline")

    logger.info("Finished the pipeline")

    # Read from .env file
    load_dotenv()
    db_name = os.getenv("POSTGRES_DB")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")

    # Connect to the database
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        
        connection.autocommit = True
        logger.info("Connected to the database")
        # Create a cursor
        cursor = connection.cursor()
        # Execute a query
        cursor.execute("SELECT version();")
        # Fetch the results of the query
        record = cursor.fetchone()
        logger.info(f"You are connected to {record}")
        # Check if the database exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';")
        exists = cursor.fetchone()
        if not exists:
            # Create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE {db_name};")
            logger.info(f"Created database {db_name}")
        else:
            logger.info(f"Database {db_name} already exists")
        # Create table if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name VARCHAR(255));")
        logger.info("Created table test_table")
        # Insert a row into the table
        cursor.execute("INSERT INTO test_table (name) VALUES ('test_value');")
        logger.info("Inserted a row into the table")
        # Fetch all rows from the table
        cursor.execute("SELECT * FROM test_table;")
        rows = cursor.fetchall()
        # Show the result
        logger.info(f"Result: {rows}")

        
    except OperationalError as e:
        logger.error(f"An error occurred while connecting to the database: {str(e)}")
    finally:
        # Close the cursor and connection if they were established
        if "cursor" in locals():    
            cursor.close()
        if "connection" in locals():
            connection.close()

if __name__ == "__main__":
    main()
