"""
{
    "layout": [
        { 
            "type": "HEADER",
            "label": "Avaliação Semestral dos Membros de RH"
            "row-span": 1,
            "col-span": full,
        },
        { 
            "type": "CONTENT",
            "rows": [
                { 
                    "type": "MEASURER",
                    "label": "Avaliador",
                    "row-span": 2,
                    "rows": [
                        "Inês Geraldes", "Inês Bastos", "Cláudia Santos"
                    ]
                },
                {
                    "type": "MEASURED",
                    "label": "Avaliado",
                    "row-span": 1,
                    "rows": [
                        "Inês Geraldes", "Inês Bastos", "Cláudia Santos"
                    ]
                },
                {
                    "type": "MEASURE",
                    "label": "1. O membro conseguiu alcançar os objetivos, estabelecidos a priori, das tarefas pelas quais foi responsável.",
                    "row-span": 1,
                    "rows": [
                        {
                            "measurer": "Inês Geraldes",
                            "measured": "Inês Geraldes",
                            "grade": 6
                        },
                        {
                            "measurer": "Inês Geraldes",
                            "measured": "Inês Geraldes",
                            "grade": 6
                        },
                        {
                            "measurer": "Inês Geraldes",
                            "measured": "Inês Geraldes",
                            "grade": 6
                        },
                    ]
                }
                ...
            ]
        }
    ]
}
"""

from typing import Union
from openpyxl import Workbook

import pandas as pd
from Layout import Layout
from Types import Type


class ExcelPrinter:
    def __init__(self, layout: Layout):
        self.layout = layout

    def print(self, filepath):
        data: dict[str: str] = self.__process_output_layout(self.layout.get_data())
        print(data)
        self.__save_file(data, filepath)
    
    """
    data = {
        'Avaliador': ['Inês Bastos', 'Catarina Milheiro', 'Gonçalo Figueiredo', 'Inês Cabral', 'Mariana Arezes', 'Mariana Oliveira', 'Paula Ferreira', 'Paulo Vieira', 'Rafaela Carvalho'],
        'Avaliado': ['Catarina Milheiro', '', 'Gonçalo Figueiredo', '', '', '', '', '', ''],
        '1. O membro cumpriu todos os prazos que foram estabelecidos para as suas tarefas?': [6, 6, 6, 6, 6, 6, 6, 4, 4],
        '2. O membro apresentou qualidade de trabalho em todas as tarefas entregues?': [6, 3, 3, 3, 3, 6, 3, 3, 3],
        '3. O membro mostrou-se prestável e amigo para com os outros membros?': [6, 3, 3, 3, 3, 6, 3, 3, 3],
        '4. O membro chegou sempre a tempo às reuniões de departamento/AR/formações/RGs e AGs marcadas?': [6, 6, 6, 3, 3, 3, 4, 4, 3],
        '5. O membro mostrou-se empenhado em desempenhar todas as suas tarefas, mesmo quando estas se apresentaram, por algum motivo, mais difíceis de realizar?': [6, 6, 3, 3, 3, 6, 3, 3, 3],
        '6. O membro mostrou-se participativo durante as reuniões (quer voluntariamente ou não), apresentando comentários construtivos?': [6, 6, 6, 3, 3, 6, 4, 3, 3],
        '7. Sentiste que algum membro, em algum momento, se demonstrou conflituoso para com alguém dentro da EPIC Júnior?': ['Não', 'Não', '', '', '', '', '', '', ''],
        'Existe algum comentário que queiras fazer sobre a avaliação que fizeste de algum membro? Se sim, qual?': ['', '', '', '', '', '', '', '', '']
    }
    """
    def __process_output_layout(self, input_data):
        data = {}
        for row in input_data:
            if row["type"] == Type.CONTENT:
                data.update(self.__process_output_layout(row["rows"]))

            elif row["type"] == Type.HEADER:
                # data.update({row.label: row.rows})
                continue
                
            elif row["type"] == Type.MEASURER or row["type"] == Type.MEASURED:
                data.update({row["label"]: row["rows"]})

            elif row["type"] == Type.MEASURE:
                grades: list[str] = []
                for measure in row["rows"]:
                    grades.append(measure["grade"])
                data.update({row["label"]: grades})

            if not row["type"]:
                data.update({row["label"]: row["rows"]})
        
        return data

    # treeData = [["Type", "Leaf Color", "Height"], ["Maple", "Red", 549], ["Oak", "Green", 783], ["Pine", "Green", 1204]]
    def __save_file(self, data: dict[str: str], filepath):
        result = []
        result.append(list(data.keys()))

        for row in data.values():
            result.append(row)

        wb = Workbook()
        ws = wb.active

        print("\n\n\n", result)
        
        for row in result:
            ws.append(row)

        wb.save(filepath)