
from Question import Question

class Measured:
    __questions = []

    def __init__(self, name: str, questions: list[Question]) -> None:
        self.name = name

        # filtrar apenas as perguntas que contêm o nome do avaliado
        self.__questions = self.__my_questions(questions).copy()
    
    def __my_questions(self, questions: list[Question]) -> list[Question]:
        return [question for question in questions if self.name.lower() in question.get_question().lower()]
    
    def get_questions(self) -> list[Question]:
        return self.__questions