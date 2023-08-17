from pandas.core.frame import DataFrame
from Stategies.AvalStrat.Question import Question


class Measurer:
    __questions = []

    def __init__(self, name: str, row_index) -> None:
        self.name = name
        self.row_index = row_index

    def evaluate(self, measured: 'Measured', file: DataFrame) -> list[Question]:
        question_to_evaluate = measured.get_questions()

        if len(question_to_evaluate) == 0:
            print(f"No questions to evaluate with {measured.get_name()}")
            exit(1)

        # cross each question col index with the row index of the measurer
        for question in question_to_evaluate:
            grade = file.iloc[self.row_index, question.get_pos_in_document()]
            question.set_grade(grade, measured, self)
        
        return question_to_evaluate.copy()
    
    def get_name(self) -> str:
        return self.name
    
    def get_grades_by_measured(self, measured_name: str, questions: list[Question]) -> list[int]:
        grades = []
        for question in questions:
            for grade, measured, measurer in question.get_grades():
                if measured.get_name() == measured_name and measurer.get_name() == self.name:
                    grades.append(grade)
        return grades


    def copy(self) -> 'Measurer':
        return Measurer(self.name, self.row_index)
    
    def __str__(self) -> str:
        return f"Measurer: {self.name}"
    
    def __eq__(self, other: "Measurer") -> bool:
        return self.name.lower() == other.name.lower()