import os
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Config import Config
import pytest


def test_reading_document():
    config = Config(True, "src/tests/testfiles/RH.json")
    interpretor: ExcelInterpretor = ExcelInterpretor(
        config=config, input_file="src/tests/testfiles/Avaliacao-Membro-RH.xlsx"
    )

    assert (
        interpretor.read_doc("src/tests/testfiles/Avaliacao-Membro-RH.xlsx") is not None
    )

    assert interpretor.find_index_and_value_of_column("Nome do avaliador")[0] == 1

    assert interpretor.find_index_and_value_of_column("Não existe") == None

    assert interpretor.get_column_values(1)[0][1] == "Rafaela Carvalho"

    assert (
        interpretor.get_target_file_name()
        == "src/tests/testfiles/Avaliacao-Membro-RH.xlsx"
    )

    assert interpretor.get_config().get_filename() == "src/tests/testfiles/RH.json"
