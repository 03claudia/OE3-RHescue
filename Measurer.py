
from Measured import Measured
import pandas as pd
from Question import Question


class Measurer:
    def __init__(self, name: str, row_index) -> None:
        self.name = name
        self.row_index = row_index

    def evaluated_with(self, measured: Measured) -> list[Question]:
        question_to_evaluate = measured.get_questions()

        # cross each question col index with the row index of the measurer
        for question in question_to_evaluate:
            grade = pd.iloc[question.pos_in_document, self.row_index]
            question.set_grade_number(grade)