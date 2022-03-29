from math import floor
from typing import List
from operator import itemgetter
from data_access import DataAccess
from random import randrange, shuffle
from datetime import datetime, timedelta


class ChooseQuestions:
    def __init__(self, data_access: DataAccess) -> None:
        self.data = data_access

    def get_unseen_questions(self, student_id: int) -> List:
        unseen_questions = []
        all_questions = self.data.get_all_questions()
        test_questions = self.data.get_all_test_questions(student_id=student_id)

        for question in all_questions:
            if question not in test_questions:
                unseen_questions.append(question)

        return unseen_questions

    def pick_random_questions(self, num_questions: int, topic_id: int = None, exc_questions: List[dict] = None) -> List[dict]:
        all_question_ids = self.data.get_question_ids(topic_id=topic_id)
        if exc_questions is not None:
            for question_id in all_question_ids:
                if question_id in exc_questions:
                    all_question_ids.remove(question_id)
        num_possible_questions = len(all_question_ids)

        chosen_questions = []
        indexes_chosen = []
        while len(indexes_chosen) != num_questions:
            question_id_index = randrange(num_possible_questions)

            if question_id_index not in indexes_chosen:
                indexes_chosen.append(question_id_index)

        for index in indexes_chosen:
            chosen_questions.append(all_question_ids[index])

        print(chosen_questions)
        return chosen_questions  # chosen questions is a list of ids e.g. [{"question_id": 1230}, {"question_id": 1044}]

    def balance_score_based_on_number_of_questions_complete(self, scores: List[float], num_questions: List[int]) -> float:
        for i in range(0, len(scores), 1):
            if num_questions[i] >= 5:
                return scores[i]
            elif num_questions[i] < 3:
                return 1
            elif num_questions[i] == 3:
                new_score = 1 - scores[i]
                return new_score * 0.8
            else:
                new_score = 1 - scores[i]
                return new_score * 0.6


    def get_decimal_percentage_score(self, questions: List[dict], multiplier: float) -> float:
        correct = 0
        incorrect = 0

        for question in questions:
            if question["correct"]:
                correct += 1
            else:
                incorrect += 1

        decimal_percentage = correct / (correct + incorrect)
        if decimal_percentage == 0:
            decimal_percentage = 1
        final_decimal = decimal_percentage * multiplier

        return final_decimal

    def get_topic_percentage_decimal_score(self, topic_questions: List[dict]) -> float:
        questions_from_topic = topic_questions

        two_weeks = []
        one_month = []
        three_months = []
        one_year = []

        for question in questions_from_topic:
            if question["update_time"] > (datetime.now() - timedelta(weeks=2)):
                two_weeks.append(question)
            elif question["update_time"] > (datetime.now() - timedelta(weeks=4)):
                one_month.append(question)
            elif question["update_time"] > (datetime.now() - timedelta(weeks=12)):
                three_months.append(question)
            else:
                one_year.append(question)

        ratios = [self.get_decimal_percentage_score(questions=two_weeks, multiplier=0.4),
                  self.get_decimal_percentage_score(questions=one_month, multiplier=0.35),
                  self.get_decimal_percentage_score(questions=three_months, multiplier=0.2),
                  self.get_decimal_percentage_score(questions=one_year, multiplier=0.05)]

        num_questions = [len(two_weeks), len(one_month), len(three_months), len(one_year)]
        final_score = self.balance_score_based_on_number_of_questions_complete(scores=ratios, num_questions=num_questions)

        return final_score

    def get_topics_ordered_by_strength(self, student_id: int) -> List[dict]:
        answered_questions = self.data.get_completed_test_questions(student_id=student_id)
        # what if no answered questions 

        topic_ids = []
        topic_percentages = []

        for question in answered_questions:
            if question['topic_id'] not in topic_ids:
                topic_ids.append(question['topic_id'])

        for topic_id in topic_ids:
            questions_in_topic = []
            for question in answered_questions:
                if question['topic_id'] == topic_id:
                    questions_in_topic.append(question)
            topic_percentages.append(self.get_topic_percentage_decimal_score(topic_questions=questions_in_topic))

        list_to_be_ordered = []
        for i in range(0, len(topic_ids), 1):
            list_to_be_ordered.append({"topic_id": topic_ids[i], "topic_score": topic_percentages[i]})

        ordered_list = sorted(list_to_be_ordered, key=itemgetter('topic_score'))

        return ordered_list

    def choose_questions_for_personalised_test(self, student_id: int, num_questions: int) -> List[dict]:
        final_questions = []  # final questions is a list of question ids
        ordered_topic_list = self.get_topics_ordered_by_strength(student_id=student_id)
        # should store a list of topics in order from weakest to strongest
        # what if there is no topic rank and the list returned is empty?

        num_of_worst_topic_questions = floor(num_questions * 0.2)
        num_of_questions_from_weaker_topics = floor(num_questions * 0.1)

        worst_topic_questions = self.pick_random_questions(num_of_worst_topic_questions, ordered_topic_list[0]["topic_id"])
        weaker_topic_1 = self.pick_random_questions(num_of_questions_from_weaker_topics, ordered_topic_list[1]["topic_id"])
        weaker_topic_2 = self.pick_random_questions(num_of_questions_from_weaker_topics, ordered_topic_list[2]["topic_id"])
        weaker_topic_3 = self.pick_random_questions(num_of_questions_from_weaker_topics, ordered_topic_list[3]["topic_id"])

        for question in worst_topic_questions:
            final_questions.append(question)
        for question in weaker_topic_1:
            final_questions.append(question)
        for question in weaker_topic_2:
            final_questions.append(question)
        for question in weaker_topic_3:
            final_questions.append(question)

        remaining_number_of_questions = num_questions - num_of_worst_topic_questions - (num_of_questions_from_weaker_topics * 3)
        set_of_random_question_ids = self.pick_random_questions(num_questions=remaining_number_of_questions,
                                                                exc_questions=final_questions)

        for question in set_of_random_question_ids:
            final_questions.append(question)

        shuffle(final_questions)
        return final_questions
