from typing import Union

class Question:
    grade_and_measurer_list: list[Union[float, int], 'Measurer']

    def __init__(self, pos_in_document, question: str) -> None:
        self.question = question
        self.pos_in_document = pos_in_document
        self.grades = []
        self.grade_and_measurer_list = []

    def __str__(self):
        return f"Question: {self.question}\nAnswers: {self.grades}\n"
    
    def get_question(self) -> str:
        return self.question
    
    def get_question_without_name(self, identifier) -> str:
        return self.question.split(identifier)[0].strip()
    
    def get_pos_in_document(self) -> int:
        return self.pos_in_document
    
    def is_question_equal(self, question):
        return question.lower() in self.question.lower()

    def set_grade(self, grade: Union[float, int], measurer: 'Measurer'):
        self.grade_and_measurer_list.append((grade, measurer))

    def get_grades(self) -> list[Union[float, int], 'Measurer']:
        return list(self.grade_and_measurer_list)
    
    def get_measurer_grade(self, measurer: 'Measurer') -> Union[float, int]:
        for grade, measurer_h in self.grade_and_measurer_list:
            if measurer_h.get_name() == measurer.get_name():
                return grade
        return -1
    
    def __copy__(self) -> 'Question':
        return Question(self.pos_in_document, self.question)