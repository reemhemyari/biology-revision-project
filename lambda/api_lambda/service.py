from typing import List
from data_access import DataAccess
from choose_question import ChooseQuestions


class Service:

    def __init__(self, data_access: DataAccess, choose_questions: ChooseQuestions):
        # constructor allows use of DataAccess and ChooseQuestions instances created in the api layer
        self.data = data_access
        self.choose_questions = choose_questions

    def __get_questions_and_options_for_test(self, test_id: int) -> List[dict]:
        questions_list = self.data.get_questions_from_test(test_id=test_id)

        for question in questions_list:
            options = self.data.get_options_for_question(question_id=question['question_id'])
            question['options'] = options

        return questions_list

    def get_modules(self) -> List[dict]:
        modules = self.data.get_modules()
        topics = self.data.get_topics()

        modules_list = []
        for i in range(len(modules)):
            module = modules[i]
            mod_topics = []

            for topic in topics:
                if topic["module_id"] == module["module_id"]:
                    mod_topics.append(topic)

            module['topics'] = mod_topics
            modules_list.append(module)

        return modules_list

    def get_topic(self, topic_id: int) -> dict:
        topic = self.data.get_topic(topic_id=topic_id)
        return topic

    def get_test(self, student_id: int, test_id: int) -> dict:
        test = self.data.get_test(student_id=student_id, test_id=test_id)
        # TODO if test does not exist maybe print error message

        # get all the questions and their corresponding options for the test
        questions_list = self.__get_questions_and_options_for_test(test_id=test_id)
        test['questions'] = questions_list

        return test

    def get_tests(self, student_id: int, complete: bool = None) -> List[dict]:

        tests = self.data.get_tests(student_id=student_id, complete=complete)

        for test in tests:  # get all the questions and their corresponding options for a test
            questions_list = self.__get_questions_and_options_for_test(test_id=test['test_id'])
            test['questions'] = questions_list

        return tests

    def make_new_test(self, student_id: int, topic_id: int = None, num_questions: int = 10) -> dict:
        test_id = self.data.new_test(student_id=student_id, topic_id=topic_id, num_questions=num_questions)  # new test record and return test id
        print("a new test has been created with the test id", test_id, "- service")

        if topic_id is None:
            question_ids = self.choose_questions.choose_questions_for_personalised_test(student_id=student_id, num_questions=num_questions)
        else:
            question_ids = self.choose_questions.pick_random_questions(num_questions=num_questions, topic_id=topic_id)

        print("these are the question ids that were picked", question_ids, "- service")
        self.data.add_questions_to_test(test_id=test_id, question_ids=question_ids)
        questions = self.__get_questions_and_options_for_test(test_id=test_id)

        for question in questions:
            options = self.data.get_options_for_question(question_id=question['question_id'])
            question['options'] = options

        test = self.data.get_test(student_id=student_id, test_id=test_id)
        test['questions'] = questions

        return test

    def is_test_complete(self, test: dict) -> bool:
        complete = False
        test_questions = self.data.get_questions_from_test(test_id=test['test_id'])

        questions_answered = 0
        for question in test_questions:
            if question['option_id'] is not None:
                questions_answered += 1

        if test['num_questions'] == questions_answered:
            complete = True

        return complete

    def calculate_points_earned(self, test_id: int) -> int:
        test_questions = self.data.get_questions_from_test(test_id=test_id)

        points_earned = 0
        for question in test_questions:
            if question['option_id'] is not None:
                option = self.data.get_option(option_id=question['option_id'])
                if option['correct']:
                    points_earned += 1

        return points_earned

    def submit_answer(self, student_id: int, test_id: int, option_id: int, question_id: int) -> None:
        self.data.update_test_question_option(test_id=test_id, option_id=option_id, question_id=question_id)

        test = self.data.get_test(student_id=student_id, test_id=test_id)

        complete = self.is_test_complete(test=test)
        if complete:
            self.data.mark_test_complete(test_id=test_id)

        points_earned = self.calculate_points_earned(test_id=test_id)
        self.data.update_points_earned(test_id=test_id, points_earned=points_earned)

    def delete_test(self, test_id) -> None:
        print("I've reached the service layer")
        self.data.delete_test(test_id=test_id)
        print("Test should be deleted now - service")
