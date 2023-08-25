import os
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Config import Config


def test_reading_document():
    config = Config(True, "src/tests/testfiles/RH.json")
    interpretor: ExcelInterpretor = ExcelInterpretor(
        config=config, input_file="src/tests/testfiles/Avaliacao-Membro-RH.xlsx"
    )

    assert (
        interpretor.read_doc("src/tests/testfiles/Avaliacao-Membro-RH.xlsx") is not None
    )

    assert interpretor.find_index_and_value_of_column("Nome do avaliador") == 0
