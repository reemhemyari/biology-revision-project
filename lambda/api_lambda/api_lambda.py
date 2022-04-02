import os
from typing import List
# from psycopg2 import Error
from data_access import DataAccess
from choose_question import ChooseQuestions
from service import Service
# from aws_lambda_powertools.event_handler import content_types
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, ProxyEventType, CORSConfig

cors_config = CORSConfig(max_age=300)
app = ApiGatewayResolver(proxy_type=ProxyEventType.ALBEvent, cors=cors_config)

data = DataAccess(host=os.environ['db_endpoint'], user=os.environ['username'], password=os.environ['password'])
questions = ChooseQuestions(data_access=data)
service = Service(data_access=data, choose_questions=questions)

student_id = 245  # temporarily hard-coded until I can do logins


# get list of modules with topics
@app.get("/modules")
def get_modules():
    modules_list = service.get_modules()
    return modules_list


# get a test
@app.get("/tests/<test_id>")
def get_test(test_id: int) -> dict:
    test = service.get_test(student_id=student_id, test_id=test_id)

    test['create_time'] = test['create_time'].isoformat()
    if test['complete']:
        test['complete_time'] = test['complete_time'].isoformat()

    return test


# get a list of tests
@app.get("/tests")
def get_tests() -> List[dict]:
    complete_str = app.current_event.get_query_string_value(name="complete")

    if complete_str is None:
        tests = service.get_tests(student_id=student_id)
    elif complete_str == 'true' or complete_str == 'false':
        complete = (complete_str == 'true')
        tests = service.get_tests(student_id=student_id, complete=complete)
    else:
        raise BadRequestError("Invalid request made")

    for test in tests:
        test['create_time'] = test['create_time'].isoformat()
        if test['complete']:
            test['complete_time'] = test['complete_time'].isoformat()

    return tests


# gets a topic
@app.get("/topics/<topic_id>")
def get_topic(topic_id: int) -> dict:
    topic = service.get_topic(topic_id=topic_id)
    return topic


# make a new test
@app.post("/tests")
def post_new_test() -> dict:

    if app.current_event.body is not None:
        topic_id = app.current_event.json_body.get("topic_id", None)
    else:
        topic_id = None

    print("a new test is about to be created - lambda")
    new_test = service.make_new_test(student_id=student_id, topic_id=topic_id)

    new_test['create_time'] = new_test['create_time'].isoformat()
    # better at this layer cuz allows manipulation in service

    print("we back to the lambda")
    return new_test


# submit answer
@app.put("/tests/<test_id>/questions/<question_id>")
def put_new_answer(test_id: int, question_id: int) -> None:
    option_id = app.current_event.json_body["option_id"]
    service.submit_answer(student_id=student_id, test_id=test_id, option_id=option_id, question_id=question_id)


@app.delete("/tests/<test_id>")
def delete_test(test_id: int) -> None:
    print("I've reached the api layer")
    service.delete_test(test_id=test_id)


def handler(event, context):
    return app.resolve(event, context)

# @app.exception_handler(Error)
# def handle_value_error(ex: Error):
#     conn.rollback()
#     return Response(
#         status_code=400,
#         content_type=content_types.APPLICATION_JSON,
#         body=f"{{\"error\":{ex}}}",
#     )

# def handler(event, context):
#     print('request: {}'.format(json.dumps(event)))
#
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM question')
#     records = cursor.fetchall()
#     return {
#         'statusCode': 200,
#         'headers': {
#             'Content-Type': 'text/plain'
#         },
#         'body': f"{records}"
#     }
