import psycopg2
from typing import List
from psycopg2.extras import RealDictCursor


class DataAccess:

    def __init__(self, host: str, user: str, password: str):
        self.conn = psycopg2.connect(
            dbname="postgres",
            host=host,
            user=user,
            password=password)

        print(f"connected : {self.conn.closed == 0}")  # if 0 then connection is open

    def get_modules(self) -> List[dict]:  # returns a list of modules
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT * FROM module')
            modules = cursor.fetchall()  # returns data outputted from query
            cursor.close()

            return modules

        except Exception:
            self.conn.rollback()
            raise

    def get_topic(self, topic_id: int) -> dict:  # returns a list of topics
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT * FROM topic WHERE topic_id=%s', (topic_id,))
            topics = cursor.fetchall()
            cursor.close()

            return topics

        except Exception:
            self.conn.rollback()
            raise

    def get_topics(self) -> List[dict]:  # returns a list of topics
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT * FROM topic')
            topics = cursor.fetchall()
            cursor.close()

            return topics

        except Exception:
            self.conn.rollback()
            raise

    def get_all_questions(self) -> List[dict]:  # returns a list question ids for all questions
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT question_id FROM question")
            all_questions = cursor.fetchall()
            cursor.close()

            return all_questions
        except Exception:
            self.conn.rollback()
            raise

    def get_options_for_question(self, question_id: int) -> List[dict]:  # gets corresponding options for question
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM option WHERE question_id=%s", (question_id,))
            options = cursor.fetchall()
            cursor.close()

            return options

        except Exception:  # if something goes wrong rollback the connection and raise an error
            self.conn.rollback()
            raise

    def get_question_ids(self, topic_id: int = None) -> List[dict]:
        if topic_id is None:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT question_id FROM question")
            question_ids = cursor.fetchall()
        else:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT question_id FROM topicquestion WHERE topic_id= %s", (topic_id,))
            question_ids = cursor.fetchall()
            print(question_ids)

        cursor.close()
        return question_ids

    def get_questions_with_id(self, question_ids: List[int]) -> List[dict]:  # returns list of specified questions
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM question WHERE question_id IN %s", (question_ids,))
        questions = cursor.fetchall()
        cursor.close()
        return questions

    def get_all_test_questions(self, student_id: int) -> List[dict]:
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT tq.*, t.student_id FROM testquestion tq JOIN test t ON "
                           "t.test_id=tq.test_id WHERE t.student_id= %s", (student_id,))
            test_questions = cursor.fetchall()
            cursor.close()

            return test_questions

        except Exception:
            self.conn.rollback()
            raise

    def get_completed_test_questions(self, student_id: int) -> List[dict]:
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT t.topic_id, tq.update_time, o.correct FROM testquestion tq JOIN option o ON "
                           "tq.option_id=o.option_id JOIN test t ON tq.test_id=t.test_id WHERE update_time > NOW() - "
                           "INTERVAL '1 YEAR' AND t.student_id=%s", (student_id,))
            test_questions = cursor.fetchall()
            cursor.close()

            return test_questions

        except Exception:
            self.conn.rollback()
            raise

    def get_questions_from_test(self, test_id: int) -> List[dict]:
        # gets list of questions specific to a test
        try:
            print(test_id)
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT q.*, tq.option_id FROM testquestion tq JOIN question q ON "
                           "q.question_id=tq.question_id WHERE tq.test_id= %s", (test_id,))
            questions = cursor.fetchall()
            cursor.close()

            return questions

        except Exception:
            self.conn.rollback()
            raise

    def get_test(self, student_id: int, test_id: int) -> dict:  # gets a test
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM test WHERE test_id= %s AND student_id= %s", (test_id, student_id))
            test = cursor.fetchone()
            cursor.close()

            if test is None:
                message = {'Error Message': 'test does not exist'}
                return message
            else:
                return test

        except Exception:
            self.conn.rollback()
            raise

    def get_tests(self, student_id: int, complete: bool = None) -> List[dict]:  # gets a list of tests
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            if complete is None:  # select all the student's tests from the database
                cursor.execute("SELECT * FROM test WHERE student_id= %s", (student_id,))
                tests = cursor.fetchall()
            else:  # select the users in/complete tests
                cursor.execute("SELECT * FROM test WHERE complete=%s AND student_id= %s", (complete, student_id))
                tests = cursor.fetchall()
            cursor.close()

            return tests

        except Exception:
            self.conn.rollback()
            raise

    def new_test(self, student_id: int, topic_id: int, num_questions: int) -> int:
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""INSERT INTO test (student_id, points_earned, num_questions, topic_id, complete, 
                           create_time) VALUES (%s, %s, %s, %s, %s, NOW()) RETURNING test_id""",
                           (student_id, 0, num_questions, topic_id, False))
            test_id_dict = cursor.fetchone()
            test_id = test_id_dict['test_id']

            self.conn.commit()
            cursor.close()

            return test_id

        except Exception:
            self.conn.rollback()
            raise

    def add_questions_to_test(self, test_id: int, question_ids: List[dict]) -> None:
        try:
            for question_id_dict in question_ids:
                cursor = self.conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute("INSERT INTO testquestion (question_id, test_id) VALUES (%s, %s)",
                               (question_id_dict['question_id'], test_id))

            self.conn.commit()

        except Exception:
            self.conn.rollback()
            raise

    def get_option(self, option_id: int) -> dict:
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM option WHERE option_id= %s", (option_id,))
            option = cursor.fetchone()
            cursor.close()

            return option

        except Exception:
            self.conn.rollback()
            raise

    def update_test_question_option(self, test_id: int, option_id: int, question_id: int) -> None:
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("UPDATE testquestion SET option_id= %s, update_time=NOW() WHERE test_id= %s AND "
                           "question_id= %s", (option_id, test_id, question_id))

            self.conn.commit()
            cursor.close()

        except Exception:
            self.conn.rollback()
            raise

    def get_test_question(self, test_id: int, question_id: int) -> dict:
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM testquestion WHERE test_id= %s AND "
                           "question_id= %s", (test_id, question_id))
            test_question = cursor.fetchone()
            cursor.close()

            return test_question

        except Exception:
            self.conn.rollback()
            raise

    def update_points_earned(self, test_id: int, points_earned: int) -> None:
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("UPDATE test SET points_earned= %s WHERE test_id= %s", (points_earned, test_id))
            self.conn.commit()
            cursor.close()

        except Exception:
            self.conn.rollback()
            raise

    def mark_test_complete(self, test_id: int) -> None:
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("UPDATE test SET complete= %s, complete_time=NOW() WHERE test_id= %s", (True, test_id))
            self.conn.commit()
            cursor.close()

        except Exception:
            self.conn.rollback()
            raise

    def delete_test(self, test_id) -> None:
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("DELETE FROM testquestion WHERE test_id=%s", (test_id,))
            cursor.execute("DELETE FROM test WHERE test_id=%s", (test_id,))
            self.conn.commit()
            cursor.close()
            print("deleted test - data")
        except Exception:
            self.conn.rollback()
            raise


    # def __get_questions_options_for_test(self, test_id: int) -> List[dict]:
    #     cursor = self.conn.cursor()
    #     cursor.execute("SELECT question_id FROM testquestion WHERE test_id= %s", (test_id,))
    #     question_ids = cursor.fetchall()
    #
    #     q_ids = []
    #     for i in question_ids:
    #         q_ids.append(i[0])
    #
    #     question_id_tuple = tuple(q_ids)
    #
    #     cursor2 = self.conn.cursor(cursor_factory=RealDictCursor)
    #     cursor2.execute("SELECT * FROM question WHERE question_id IN %s", (question_id_tuple,))
    #     questions = cursor2.fetchall()
    #
    #     cursor4 = self.conn.cursor(cursor_factory=RealDictCursor)
    #     cursor4.execute("SELECT * FROM option WHERE question_id IN %s", (question_id_tuple,))
    #     options = cursor4.fetchall()
    #
    #     for question in questions:
    #         question_options = []
    #         for option in options:
    #             if option['question_id'] == question['question_id']:
    #                 question_options.append(option)
    #
    #         question['options'] = question_options
    #
    #     return questions
    #
    # def get_question_ids(self, topic_id: int = None) -> List[int]:
    #     if topic_id is None:
    #         cursor = self.conn.cursor("SELECT question_id FROM question")
    #         question_ids = cursor.fetchall()  # I'm not sure whether this is going to be a list
    #     else:
    #         cursor = self.conn.cursor("SELECT question_id FROM question WHERE topic_id= %s", (topic_id,))
    #         question_ids = cursor.fetchall()
    #
    #     return question_ids
    #
    # def get_questions_with_id(self, question_ids: List[int]) -> List[dict]:
    #     # the id list will come from the randomly picked questions from choose questions
    #     cursor = self.conn.cursor(cursor_factory=RealDictCursor)
    #     cursor.execute("SELECT * FROM question WHERE question_id IN %s", (question_ids,))
    #     questions = cursor.fetchall()
    #     return questions
    #
    # def get_modules(self) -> List[dict]:
    #     try:
    #         cursor = self.conn.cursor(cursor_factory=RealDictCursor)
    #         cursor.execute('SELECT * FROM module')
    #         modules = cursor.fetchall()  # returns data outputted from query
    #
    #         cursor2 = self.conn.cursor(cursor_factory=RealDictCursor)
    #         cursor2.execute('SELECT * FROM topic')
    #         topics = cursor2.fetchall()
    #
    #         modules_list = []
    #         for i in range(len(modules)):
    #             module = modules[i]
    #             mod_topics = []
    #
    #             for topic in topics:
    #                 if topic["module_id"] == module["module_id"]:
    #                     mod_topics.append(topic)
    #
    #             module['topics'] = mod_topics
    #             modules_list.append(module)
    #         return modules_list
    #
    #     except Exception:
    #         self.conn.rollback()
    #         raise
    #
    # def get_test(self, student_id: int, test_id: int) -> dict:
    #     try:
    #         # select a specific student test
    #         cursor = self.conn.cursor(cursor_factory=RealDictCursor)
    #         cursor.execute("SELECT * FROM test WHERE test_id= %s AND student_id= %s", (test_id, student_id))
    #         test = cursor.fetchone()  # need to consider what happens if test does not exist
    #
    #         # get all the questions and their corresponding options for the test
    #         questions = self.__get_questions_options_for_test(test_id)
    #         test['questions'] = questions
    #         return test
    #
    #     except Exception:
    #         self.conn.rollback()
    #         raise
    #
    # def get_tests(self, student_id: int, complete: bool = None) -> List[dict]:
    #     try:
    #         cursor = self.conn.cursor(cursor_factory=RealDictCursor)
    #         if complete is None:  # select all the student's tests from the database
    #             cursor.execute("SELECT * FROM test WHERE student_id= %s", (student_id,))
    #             tests = cursor.fetchall()
    #         else:  # select the users in/complete tests
    #             cursor.execute("SELECT * FROM test WHERE complete=%s AND student_id= %s", (complete, student_id))
    #             tests = cursor.fetchall()
    #
    #         for test in tests:  # get all the questions and their corresponding options for a test
    #             questions = self.__get_questions_options_for_test(test['test_id'])
    #             test['questions'] = questions
    #
    #         return tests
    #
    #     except Exception:  # if something goes wrong rollback the connection and raise an error
    #         self.conn.rollback()
    #         raise
    #
    # def make_new_test(self, student_id: int, question_ids: List[int], topic_id: int = None) -> dict:
    #     # how does the list of ids get passed in ?
    #     # add new test record to the test table
    #     cursor = self.conn.cursor(cursor_factory=RealDictCursor)
    #     cursor.execute("INSERT INTO test (student_id, points_earned, num_questions, topic_id, complete, date_time) "
    #                    "VALUES %s RETURNING test_id", (student_id, 0, 10, topic_id, False, None))
    #     # this might not work because you haven't given a test_id
    #     test_id = cursor.fetchone()
    #
    #     # add each question id in the new test to a test question record
    #     for question_id in question_ids:
    #         cursor = self.conn.cursor(cursor_factory=RealDictCursor)
    #         cursor.execute("INSERT INTO testquestion (question_id, test_id, option_id, date_time) VALUES %s",
    #                        (question_id, test_id, None, None))
    #
    #     # go fetch that test and return it
    #     test = self.get_test(student_id, test_id)
    #     return test
    #
    # def submit_answer(self, student_id: int, test_id: int, option_id: int) -> None:
    #     # for the specific test question, update option_id
    #     # -> you can get the question id from the option record
    #
    #     # if option with option_id is correct, add one to points earned
    #
    #     # you need a condition for if it is the last question -> how would you know ??
    #     # if it is the last question change complete to true
    #     pass
