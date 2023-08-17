
import re
from typing import Union
from Stategies.AvalStrat.Measurer import Measurer
from Stategies.AvalStrat.Question import Question

class Measured:
    __questions = []

    def __init__(self, name: str, all_questions: list[Question]) -> None:
        self.name = name
        self.__questions = self.__my_questions(all_questions)
    
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
    
    def get_grades_by_measurer(self, measurer_name: str) ->  list[Union[float, int]]:
        # search for the question
        grades = []
        for question in self.__questions:
            for grade, measured, measurer in question.get_grades():
                if measured.get_name() == self.name and measurer_name == measurer.get_name():
                    grades.append(grade)
        return grades
    
    def get_measurers(self) -> list[Measurer]:
        measurers = []
        for question in self.__questions:
            for _, _, measurer in question.get_grades():
                if measurer not in measurers:
                    measurers.append(measurer)
        return measurers
    
    def get_name(self) -> str:
        return self.name

    def __str__(self) -> str:
        var = f"Measured: {self.name}\nQuestions: [\n"
        for question in self.__questions:
            var += f"{question}\n"
        var += "]"
        return var
    