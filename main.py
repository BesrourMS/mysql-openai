import mysql.connector
from mysql.connector import Error
import openai
from typing import List, Tuple, Optional
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection
def connect_db() -> Optional[mysql.connector.connection.MySQLConnection]:
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        if connection.is_connected():
            logging.info("Connected to MySQL database")
            return connection
    except Error as err:
        logging.error(f"Database connection error: {err}")
    return None

# OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

def fetch_data_from_db(connection: mysql.connector.connection.MySQLConnection, 
                       batch_size: int = 1000) -> List[Tuple]:
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, feedback FROM customer_feedback WHERE response IS NULL")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

def process_data_with_openai(data: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful customer service assistant. Provide a brief, empathetic response to the following customer feedback:"},
                {"role": "user", "content": data}
            ],
            max_tokens=100
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return ""

def update_db_with_responses(connection: mysql.connector.connection.MySQLConnection, 
                             data: List[Tuple[str, int]]) -> None:
    update_query = "UPDATE customer_feedback SET response = %s WHERE id = %s"
    try:
        with connection.cursor() as cursor:
            cursor.executemany(update_query, data)
        connection.commit()
    except Error as e:
        logging.error(f"Database update error: {e}")
        connection.rollback()

def main():
    db_connection = connect_db()
    if not db_connection:
        return

    try:
        for batch in fetch_data_from_db(db_connection):
            processed_data = []
            for row in batch:
                id, feedback = row
                response = process_data_with_openai(feedback)
                processed_data.append((response, id))
            
            update_db_with_responses(db_connection, processed_data)
            logging.info(f"Processed and updated {len(processed_data)} records")

    except Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        if db_connection and db_connection.is_connected():
            db_connection.close()
            logging.info("MySQL connection is closed")

if __name__ == "__main__":
    main()
