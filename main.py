import mysql.connector
import openai

# Database connection
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="your_host",
            user="your_username",
            password="your_password",
            database="your_database"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# OpenAI API Key
openai.api_key = "your_openai_api_key"

def fetch_data_from_db(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM your_table")
    rows = cursor.fetchall()
    return rows

def process_data_with_openai(data):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=data,
        max_tokens=50
    )
    return response.choices[0].text.strip()

def update_db_with_response(connection, original_data, response):
    cursor = connection.cursor()
    update_query = "UPDATE your_table SET response_column = %s WHERE data_column = %s"
    cursor.execute(update_query, (response, original_data))
    connection.commit()

# Main workflow
db_connection = connect_db()
if db_connection:
    data_rows = fetch_data_from_db(db_connection)
    for row in data_rows:
        original_data = row[0]  # Adjust index based on your table structure
        response = process_data_with_openai(original_data)
        update_db_with_response(db_connection, original_data, response)

    if db_connection.is_connected():
        db_connection.close()
        print("MySQL connection is closed")
