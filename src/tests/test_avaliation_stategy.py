from Config import Config
from Interpretors.ExcelInterpretor import ExcelInterpretor
from Log.Logger import Logger
from Stategies.AvalStrat.AvaliationStrategy import AvaliationStrategy

def test_avaliation_stategy():
    config: Config = Config(True, "src/tests/testfiles/RH.json")
       
    excel_interpretor: ExcelInterpretor = ExcelInterpretor(config, "src/tests/testfiles/Avaliacao-Membro-RH.xlsx")

    stategy:AvaliationStrategy = AvaliationStrategy(excel_interpretor, "[")
    
    # TODO: Adicionar mais testes de jeito                                   
    assert stategy.name_divider == "["
    
