import os
import json
import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    host=os.environ['db_endpoint'],
    user=os.environ['username'],
    password=os.environ['password'])

print(os.environ['db_endpoint'], os.environ['username'])
print(f"connected : {conn.closed == 0}")  # if 0 then connection is open


def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM question')
    records = cursor.fetchall()
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f"{records}"
    }
