from Config import Config
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Stategies.AvalStrat.AvaliationStrategy import AvaliationStrategy
from Types import Type
import pytest
from Stategies.AvalStrat.Question import Question

def test_avaliation_stategy():
    config: Config = Config(True, "src/tests/testfiles/RH.json")
    excel_interpretor: ExcelInterpretor = ExcelInterpretor(config, "src/tests/testfiles/test_avaliation_stategy.py")
    stategy:AvaliationStrategy = AvaliationStrategy(excel_interpretor, "[")

    result: list[Question] = stategy.parse()
    assert result == 0
