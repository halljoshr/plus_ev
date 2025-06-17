import psycopg2
import os
from dotenv import load_dotenv

# If you see a linter error for 'dotenv', install it with: pip install python-dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=os.environ.get("DB_PORT", "5432"),
)

cur = conn.cursor()
cur.execute("SELECT * FROM pev_app_plusev")
rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()
