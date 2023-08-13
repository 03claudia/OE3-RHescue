


from typing import Union


class Question:
    grade: Union[float, int]
    measurer: 'Measurer'

    def __init__(self, pos_in_document, question: str) -> None:
        self.question = question
        self.pos_in_document = pos_in_document
        self.grades = []
        self.measurer = None

    def __str__(self):
        return f"Question: {self.question}\nAnswers: {self.grades}\n"
    
    def get_question(self) -> str:
        return self.question
    
    def get_pos_in_document(self) -> int:
        return self.pos_in_document
    
    def is_question_equal(self, question):
        return question.lower() in self.question.lower()

    def set_grade_number(self, grade: Union[float, int], measurer: 'Measurer'):
        if not grade < 0:
            self.measurer = measurer
            self.grade = grade

    def get_grade(self) -> Union[float, int]:
        return self.grade
    
    def get_measurer(self) -> 'Measurer':
        return self.measurer