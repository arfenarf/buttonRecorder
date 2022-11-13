from fastapi import FastAPI
import psycopg2
from datetime import datetime, timezone
import os

app = FastAPI()
DB_PASSWORD = os.environ.get('TOFINO_POSTGRES_PW')
def get_db_connection():
    connection = psycopg2.connect(host='tofino.local',
                                  dbname='kgw_data',
                                  user='postgres',
                                  password=DB_PASSWORD,
                                  port=25432)
    return connection

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/button")
async def save_button_time():
    with get_db_connection() as connection:
        with connection.cursor() as curs:
            utc_dt = datetime.now(timezone.utc)
            curs.execute("""
                INSERT INTO button_presses (date_time_pressed)
                VALUES (%s)
            """, (utc_dt, ))
        curs.close()

    return {"messages": f"posted {utc_dt}"}
