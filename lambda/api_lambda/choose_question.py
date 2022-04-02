from math import floor
from typing import List
from operator import itemgetter
from data_access import DataAccess
from random import randrange, shuffle
from datetime import datetime, timedelta, timezone


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

    def pick_random_questions(self, num_questions: int, topic_id: int = None, exc_questions: List[dict] = None) -> List[
        dict]:
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

        for i in indexes_chosen:
            chosen_questions.append(all_question_ids[i])

        print(chosen_questions, "-pick random questions")
        return chosen_questions  # chosen questions is a list of ids e.g. [{"question_id": 1230}, {"question_id": 1044}]

    def balance_score_based_on_number_of_questions_complete(self, questions_complete: int, score: float) -> float:
        if questions_complete < 3:
            return 1  # because not enough history, give the user a perfect score
        elif questions_complete == 3:
            difference_from_perfect_score = 1 - score
            return score + (difference_from_perfect_score * 0.8)
        elif questions_complete == 4:
            difference_from_perfect_score = 1 - score
            return score + (difference_from_perfect_score * 0.6)
        else:
            return score

    def get_ratio_of_correct_answers_as_decimal(self, questions: List[dict]) -> float:
        correct = 0
        incorrect = 0

        for question in questions:
            if question["correct"]:
                correct += 1
            else:
                incorrect += 1

        if correct + incorrect == 0:
            decimal_score = 1
        else:
            decimal_score = correct / (correct + incorrect)

        print("decimal score:", decimal_score)
        return decimal_score

    def get_topic_score(self, questions: List[dict]) -> float:
        two_weeks = []
        one_month = []
        three_months = []
        one_year = []

        for question in questions:
            if question["update_time"] > (datetime.now(timezone.utc) - timedelta(weeks=2)):
                two_weeks.append(question)
            elif question["update_time"] > (datetime.now(timezone.utc) - timedelta(weeks=4)):
                one_month.append(question)
            elif question["update_time"] > (datetime.now(timezone.utc) - timedelta(weeks=12)):
                three_months.append(question)
            else:
                one_year.append(question)

        # calculate fraction for each time period
        two_week_decimal_score = self.get_ratio_of_correct_answers_as_decimal(questions=two_weeks)
        one_month_decimal_score = self.get_ratio_of_correct_answers_as_decimal(questions=one_month)
        three_months_decimal_score = self.get_ratio_of_correct_answers_as_decimal(questions=three_months)
        one_year_decimal_score = self.get_ratio_of_correct_answers_as_decimal(questions=one_year)

        # multiply that number based on the number of questions complete
        two_week_balanced_score = self.balance_score_based_on_number_of_questions_complete(
            questions_complete=len(two_weeks), score=two_week_decimal_score)
        one_month_balanced_score = self.balance_score_based_on_number_of_questions_complete(
            questions_complete=len(one_month), score=one_month_decimal_score)
        three_month_balanced_score = self.balance_score_based_on_number_of_questions_complete(
            questions_complete=len(three_months), score=three_months_decimal_score)
        one_year_balanced_score = self.balance_score_based_on_number_of_questions_complete(
            questions_complete=len(one_year), score=one_year_decimal_score)

        # multiply that number based on when it was complete
        # add all the numbers together
        score = (two_week_balanced_score * 0.4) + (one_month_balanced_score * 0.35) + (
                three_month_balanced_score * 0.2) + (one_year_balanced_score * 0.05)

        return score

    def get_topics_ordered_by_strength(self, student_id: int) -> List[dict]:
        answered_questions = self.data.get_completed_test_questions(student_id=student_id)

        questions_in_topics = {}
        for question in answered_questions:
            if question['topic_id'] not in questions_in_topics.keys():
                questions_in_topics[question['topic_id']] = [question]
            else:
                questions_in_topics[question['topic_id']].append(question)

        list_to_be_ordered = []

        for topic_id in questions_in_topics.keys():
            print(topic_id)
            topic_score = self.get_topic_score(questions=questions_in_topics[topic_id])
            print("appending the following:", {"topic_id": topic_id, "topic_score": topic_score},
                  "- topics ordered by strength")
            list_to_be_ordered.append({"topic_id": topic_id, "topic_score": topic_score})

        ordered_list = sorted(list_to_be_ordered, key=itemgetter('topic_score'))

        return ordered_list

    def find_min_value(self, four: int, length_of_list: int) -> int:
        if four < length_of_list:
            return four
        else:
            return length_of_list

    def choose_questions_for_personalised_test(self, student_id: int, num_questions: int) -> List[dict]:
        print("choose questions")
        final_questions = []
        ordered_topic_list = self.get_topics_ordered_by_strength(student_id=student_id)
        print("ordered list:", ordered_topic_list, "- choose questions")

        if len(ordered_topic_list) <= 4:
            # the 'best' topic is removed if the list contains four or less topics
            # we don't know how much better or worse it is in comparison to the uncompleted topics
            ordered_topic_list.pop()

        ordered_topic_list = [topic_and_score for topic_and_score in ordered_topic_list if
                              topic_and_score['topic_score'] != 1.0]

        print("ordered list post removal of data:", ordered_topic_list)

        num_of_worst_topic_questions = floor(num_questions * 0.2)
        num_of_questions_from_weaker_topics = floor(num_questions * 0.1)

        if len(ordered_topic_list) > 1:
            print("worst topic questions")
            final_questions = self.pick_random_questions(num_of_worst_topic_questions,
                                                         ordered_topic_list[0]["topic_id"])

            min_length_value = self.find_min_value(four=4, length_of_list=len(final_questions))
            print("min value", min_length_value)
            for index in range(1, min_length_value, 1):
                print("weaker topic", index)
                weaker_topic_questions = self.pick_random_questions(num_of_questions_from_weaker_topics,
                                                                    ordered_topic_list[index]["topic_id"])
                for question_id in weaker_topic_questions:
                    final_questions.append(question_id)

        remaining_num_of_questions = num_questions - len(final_questions)
        print("remaining questions")
        set_of_random_question_ids = self.pick_random_questions(num_questions=remaining_num_of_questions,
                                                                exc_questions=final_questions)
        for question_id in set_of_random_question_ids:
            final_questions.append(question_id)

        shuffle(final_questions)
        return final_questions
