import os
import json
import psycopg2

# add logging
# try it without a db name
# try with 'postgres'
print(os.environ['db_endpoint'], os.environ['username'])
conn = psycopg2.connect(
     host=os.environ['db_endpoint'],
     user=os.environ['username'],
     password=os.environ['password']
 )

cur = conn.cursor()


def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    cur.execute("CREATE DATABASE biology-revision")
    cur.execute("SELECT table_name FROM information_schema.tables")
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f"{os.environ['username']}, {os.environ['db_endpoint']}"
    }
