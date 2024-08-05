# Customer Feedback Response Automation

This project automates the process of responding to customer feedback using OpenAI's GPT model. It fetches customer feedback from a MySQL database, generates appropriate responses using the OpenAI API, and updates the database with these responses.

## Features

- Connects to a MySQL database to fetch customer feedback
- Uses OpenAI's GPT-3.5-turbo model to generate personalized responses
- Batch processing for efficient handling of large datasets
- Updates the database with AI-generated responses
- Implements error handling and logging for robustness

## Prerequisites

- Python 3.7+
- MySQL database
- OpenAI API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/besrourms/mysql-openai.git
   cd mysql-openai
   ```

2. Install the required Python packages:
   ```
   pip install mysql-connector-python openai python-dotenv
   ```

3. Set up your MySQL database:
   ```sql
   CREATE DATABASE IF NOT EXISTS example_db;
   USE example_db;

   CREATE TABLE IF NOT EXISTS customer_feedback (
       id INT AUTO_INCREMENT PRIMARY KEY,
       feedback TEXT NOT NULL,
       response TEXT
   );
   ```

4. Create a `.env` file in the project root directory with the following content:
   ```
   DB_HOST=your_mysql_host
   DB_USER=your_mysql_username
   DB_PASSWORD=your_mysql_password
   DB_NAME=example_db
   OPENAI_API_KEY=your_openai_api_key
   ```
   Replace the placeholder values with your actual MySQL credentials and OpenAI API key.

## Usage

1. Ensure your MySQL database is running and accessible.

2. Run the main script:
   ```
   python main.py
   ```

3. The script will process all customer feedback entries that don't have a response, generate responses using the OpenAI API, and update the database.

4. You can view the results by querying your database:
   ```sql
   SELECT * FROM customer_feedback;
   ```

## Configuration

You can adjust the following parameters in the `main.py` file:

- `batch_size` in the `fetch_data_from_db` function to control how many records are processed at once.
- `max_tokens` in the `process_data_with_openai` function to adjust the length of generated responses.

## Error Handling and Logging

The script includes error handling for database operations and API calls. Logs are printed to the console, providing information about the script's progress and any errors encountered.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Disclaimer

This project uses the OpenAI API to generate responses. Ensure that your use of the API complies with OpenAI's use-case policies and that you monitor your API usage to manage costs.
