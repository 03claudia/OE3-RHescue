from Config import Config
from Types import Type
import pytest


def test_config():
    config: Config = Config(True, "src/tests/testfiles/RH.json")

    with pytest.raises(SystemExit):
        config = Config(True, "src/tests/testfiles/RH1.json")

    config: Config = Config(True, "src/tests/testfiles/RH.json")

    assert config.get_filename() == "src/tests/testfiles/RH.json"

    assert config.get_data_as_json() is not None
    assert config.get_data()[0]["label"] == "Carimbo de data/hora"

    assert config.get_type(Type.CONTENT) == []

    assert config.get_type(Type.MEASURER)[0]["label"] == "Nome do avaliador"

    output_data = config.get_data("output")
    assert len(config.get_type(Type.MEASURER, output_data)) > 2
    
