from random import randrange
from typing import List
from data_access import DataAccess


class ChooseQuestions:
    def __init__(self, data_access: DataAccess) -> None:
        self.data = data_access

    def get_questions(self, student_id: int, topic_id: int = None) -> List[dict]:
        pass

    def pick_random_questions(self, num_questions: int, topic_id: int = None) -> List[dict]:
        all_question_ids = self.data.get_question_ids(topic_id=topic_id)
        num_possible_questions = len(all_question_ids)

        chosen_questions = []  #TODO fix this so it always puts 10 questions in!!!!!
        indexes_chosen = []
        for i in range(0, num_questions):
            question_id_index = randrange(num_possible_questions)

            if question_id_index not in indexes_chosen:
                indexes_chosen.append(question_id_index)

        for index in indexes_chosen:
            chosen_questions.append(all_question_ids[index])

        print(chosen_questions)
        return chosen_questions
