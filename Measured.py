
import re
from Question import Question

class Measured:
    __questions = []

    def __init__(self, name: str, all_questions: list[Question]) -> None:
        self.name = name
        self.__questions = self.__my_questions(all_questions).copy()
    
    def __my_questions(self, questions: list[Question]) -> list[Question]:
        result: list[Question] = []
        for question in questions:
            cleaned_name = re.sub(r'\W+', '', self.name.strip().lower())
            cleaned_question = re.sub(r'\W+', '', question.get_question().lower())
            if cleaned_name in cleaned_question:
                result.append(question)
        return result

    def get_questions(self) -> list[Question]:
        return self.__questions
    
    def get_name(self) -> str:
        return self.name

    def __str__(self) -> str:
        return f"Measured: {self.name}\nQuestions: {self.__questions}\n"
    