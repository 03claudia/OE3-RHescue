from Utils.ToAscii import to_ascii
from typing import Union
from Stategies.AvalStrat.Measurer import Measurer
from Stategies.AvalStrat.Question import Question
from Types import Type

class Measured:
    __questions = []

    def __init__(self, name: str, all_questions: list[Question]) -> None:
        self.name = name
        self.__questions = self.__my_questions(all_questions)
    
    def __my_questions(self, questions: list[Question]) -> list[Question]:
        result: list[Question] = []
        num_obs = 0
        for question in questions:

            if question.get_question_type() == Type.OBSERVATION:
                num_obs += 1
                result.append(question)
            
            cleaned_name = to_ascii(self.name.lower())
            if cleaned_name in to_ascii(question.get_question().lower()):
                result.append(question)
        
        if len(result) <= num_obs:
            print(f"{self.name} não tem perguntas para ser avaliada.")
            exit(1)
        return result
    
    def get_number_of_question(self):
        return len(self.__questions)

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
    
