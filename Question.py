

class Question:
    grades: list[tuple[float | int, 'Measurer']]

    def __init__(self, pos_in_document, question) -> None:
        self.question = question
        self.pos_in_document = pos_in_document
        self.grades = []

    def __str__(self):
        return f"Question: {self.text}\nAnswer: {self.answer}\n"
    
    def get_question(self) -> str:
        return self.question
    
    def is_question_equal(self, question):
        return question.lower() in self.question.lower()

    def set_grade_number(self, grade: tuple[float | int, "Measurer"]):
        if not grade[0] < 0:
            self.grades.append(grade)

    def set_grade_string(self, grade: tuple[str, "Measurer"]):
        if grade[0].lower() == "n/a":
            self.grades[0] = -1
        else:
            self.grades = float(grade.replace(",", "."))