from typing import Union

class Question:
    grade_and_measurer_list: list[Union[float, int], 'Measured', 'Measurer']

    def __init__(self, pos_in_document, question: str) -> None:
        self.question = question
        self.pos_in_document = pos_in_document
        self.grades = []
        self.grade_and_measurer_list = []

    def __str__(self):
        question = f"\nQuestion: {self.question}"
        for grade, measured, measurer in self.grade_and_measurer_list:
            question += f"\n| {measurer.get_name()} - {measured.get_name()} - {grade} |"
        return question
    
    def __eq__(self, other: 'Question') -> bool:
        return self.question.lower() == other.question.lower()
    
    def get_question(self) -> str:
        return self.question
    
    def get_measured(self) -> list["Measured"]:
        measured_list = []
        for grade, measured, measurer in self.grade_and_measurer_list:
            if measured not in measured_list:
                measured_list.append(measured)
        return measured_list
    
    def get_question_without_name(self, identifier) -> str:
        return self.question.split(identifier)[0].strip()
    
    def get_pos_in_document(self) -> int:
        return self.pos_in_document
    
    def is_question_equal(self, question):
        return question.lower() in self.question.lower()

    def set_grade(self, grade: Union[float, int], measured: 'Measured', measurer: 'Measurer'):
        self.grade_and_measurer_list.append((grade, measured, measurer))

    def get_grades(self) -> list[Union[float, int], 'Measured', 'Measurer']:
        return list(self.grade_and_measurer_list)
    
    def get_measurer_grade(self, measurer: 'Measurer') -> Union[float, int]:
        for grade, measurer_h in self.grade_and_measurer_list:
            if measurer_h.get_name() == measurer.get_name():
                return grade
        return -1
    
    def get_grade_by_measurer(self, measurer: 'Measurer') -> list[Union[float, int], "Measured"]:
        result = []
        for grade, measured, measurer_h in self.grade_and_measurer_list:
            if measurer_h.get_name() == measurer.get_name():
                result.append((grade, measured))
        return result
    
    def __copy__(self) -> 'Question':
        return Question(self.pos_in_document, self.question)
    
    def iter_grades(self, measured: 'Measured', measurer: 'Measurer'):
        for grade, measured_h, measurer_h in self.grade_and_measurer_list:
            if measured_h.get_name() == measured.get_name() and measurer_h.get_name() == measurer.get_name():
                yield grade

    def mix_questions(question_list) -> list["Question"]:
        mixed_questions = []

        for question in question_list:
            q: Question = Question(0, question.get_question_without_name("["))
            for question in question_list:
                if q.is_question_equal(question.get_question_without_name("[")):
                    for grade, measured, measurer in question.get_grades():
                        q.set_grade(grade, measured, measurer)

            if q not in mixed_questions:
                mixed_questions.append(q)
            
        return mixed_questions