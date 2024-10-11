import mysql.connector
from time import sleep
import requests
import logging

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG,)
logger = logging.getLogger(__name__)


URL = 'http://ai-myollama:11434/api/generate'
DATA = {
    "model": "llama2",
    "prompt": "Why is the sky blue?",
    "stream": False,
}

add_response = ("INSERT INTO responses "
                "(model, created_at, response) "
                "VALUES (%s, %s, %s)")

def get_connection():
    return mysql.connector.connect(
        host="database",
        port=3306,
        user="testuser",
        password="testpassword",
        database="ollama_db"
    )


def get_response():
    response = requests.post(URL, json=DATA)
    return response.json()


def save_response(response, cursor):
    model = response['model']
    created = response['created_at']
    response = response['response']
    data_response = (model, created, response)
    logger.info(f"Model: {model} response {response}")
    cursor.execute(add_response, data_response)
    logger.info("data added to db")
    

def check_response(cursor):
    cursor.execute("SELECT * FROM responses")
    for (model, created_at, response) in cursor:
        logger.info(f"Model: {model} created at {created_at} response {response}")


def main():
    # wait for db container to start
    sleep(10)
    connection = get_connection()
    cursor = connection.cursor()
    logger.info("got connection: %s", connection)
    # wait for llm container to start
    sleep(10)
    response = get_response()
    save_response(response, cursor)
    connection.commit()
    check_response(cursor)
    cursor.close()
    connection.close()

    
if __name__ == '__main__':
    main()