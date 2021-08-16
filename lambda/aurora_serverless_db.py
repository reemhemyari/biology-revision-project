import json
import os
# import psycopg2

# psycopg2.connect(
#     database=os.environ['dsdds'],
#     user="reemhemyari",
#     password=""
# )


def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f"{os.environ['username']}, {os.environ['db_endpoint']}"
    }
