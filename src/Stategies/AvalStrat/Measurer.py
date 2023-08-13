from pandas.core.frame import DataFrame
from Stategies.AvalStrat.Measured import Measured

from Stategies.AvalStrat.Question import Question


class Measurer:
    def __init__(self, name: str, row_index) -> None:
        self.name = name
        self.row_index = row_index

    def evaluate(self, measured: Measured, file: DataFrame) -> list[Question]:
        question_to_evaluate = measured.get_questions()

        if len(question_to_evaluate) == 0:
            print(f"No questions to evaluate with {measured.get_name()}")
            exit(1)

        # cross each question col index with the row index of the measurer
        for question in question_to_evaluate:
            grade = file.iloc[self.row_index, question.get_pos_in_document()]
            question.set_grade_number(grade, self)
        
        return question_to_evaluate.copy()
    
    def get_name(self) -> str:
        return self.name
    
    def copy(self) -> 'Measurer':
        return Measurer(self.name, self.row_index)
    
    def __str__(self) -> str:
        return f"Measurer: {self.name}"