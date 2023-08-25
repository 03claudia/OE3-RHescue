import os
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Config import Config


def test_reading_document():
    current_path = os.path.dirname(os.path.abspath(__file__))
    print("curr path:", current_path)
    config = Config(True, "src/tests/testfiles/RH.json")
    interpretor: ExcelInterpretor = ExcelInterpretor(
        config=config, input_file="src/tests/testfiles/Avaliacao-Membro-RH.xlsx"
    )

    assert (
        interpretor.read_doc("src/tests/testfiles/Avaliacao-Membro-RH.xlsx") is not None
    )
