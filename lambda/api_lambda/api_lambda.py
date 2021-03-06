import os
from typing import List
from service import Service
from data_access import DataAccess
from choose_question import ChooseQuestions
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, ProxyEventType, CORSConfig

cors_config = CORSConfig(max_age=300)
app = ApiGatewayResolver(proxy_type=ProxyEventType.ALBEvent, cors=cors_config)

# instances of the different classes get created
data = DataAccess(host=os.environ['db_endpoint'], user=os.environ['username'], password=os.environ['password'])
questions = ChooseQuestions(data_access=data)
service = Service(data_access=data, choose_questions=questions)

# temporarily hard-coded variables that'll be passed in until further development complete
student_id = 245
num_questions = 10


# get list of modules with topics
@app.get("/modules")
def get_modules():
    modules_list = service.get_modules(num_questions=num_questions)
    return modules_list


# get a test
@app.get("/tests/<test_id>")
def get_test(test_id: int) -> dict:
    test = service.get_test(student_id=student_id, test_id=test_id)

    test['create_time'] = test['create_time'].isoformat()  # function converts date time object into string
    if test['complete']:
        test['complete_time'] = test['complete_time'].isoformat()

    return test


# get a list of tests
@app.get("/tests")
def get_tests() -> List[dict]:
    # gets the value that follows the query parameter complete
    complete_str = app.current_event.get_query_string_value(name="complete")

    if complete_str is None:
        tests = service.get_tests(student_id=student_id)
    elif complete_str == 'true' or complete_str == 'false':
        complete = (complete_str == 'true')  # sets complete to the boolean value returned from the comparison
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
        topic_id = app.current_event.json_body.get("topic_id", None)  # gets the topic id from the request body
    else:
        topic_id = None  # sets topic id to None if a request body is not given

    new_test = service.make_new_test(student_id=student_id, topic_id=topic_id, num_questions=num_questions)

    new_test['create_time'] = new_test['create_time'].isoformat()

    return new_test


# submit an answer
@app.put("/tests/<test_id>/questions/<question_id>")
def put_new_answer(test_id: int, question_id: int) -> None:
    option_id = app.current_event.json_body["option_id"]
    service.submit_answer(student_id=student_id, test_id=test_id, option_id=option_id, question_id=question_id)


# delete a test
@app.delete("/tests/<test_id>")
def delete_test(test_id: int) -> None:
    service.delete_test(test_id=test_id)


def handler(event, context):
    return app.resolve(event, context)
