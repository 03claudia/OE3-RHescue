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
    settings = "_settings"
    headers = "_headers"
    content = "_content"

    def __init__(self, layout: Layout):
        self.layout = layout

    def print(self, filepath):
        data: dict[str: str] = self.__process_output_layout(self.layout)
        self.__save_file(data, filepath)
    
    """
    data = {
        'Rafaela Carvalho': {
            'Catarina Milheiro': '6', 
            'Gonçalo Figueiredo': '5', 
            'Inês Cabral': '5'
        }, 
        'Paula Ferreira': {
            'Catarina Milheiro': '6', 
            'Gonçalo Figueiredo': '4', 
            'Inês Cabral': '4'
        }, 
        'Mariana Oliveira': {
            'Catarina Milheiro': '6', 
            'Gonçalo Figueiredo': '3', 
            'Inês Cabral': '5'
        }, 
        'Inês Cabral': {
            'Catarina Milheiro': '6', 
            'Gonçalo Figueiredo': '6', 
            'Inês Cabral': '6'
        }, 
        'Mariana Arezes': {
            'Catarina Milheiro': '6', 
            'Gonçalo Figueiredo': '5', 
            'Inês Cabral': '6'
        }, 
        'Paulo Vieira': {
            'Catarina Milheiro': '6', 
            'Gonçalo Figueiredo': '5', 
            'Inês Cabral': '5'
        }, 
        'Gonçalo Figueiredo': {'Catarina Milheiro': '6', 'Gonçalo Figueiredo': '4', 'Inês Cabral': '6'}, 'Catarina Milheiro': {'Catarina Milheiro': '6', 'Gonçalo Figueiredo': '4', 'Inês Cabral': '4'}, 'Inês Bastos': {'Catarina Milheiro': '6', 'Gonçalo Figueiredo': '4', 'Inês Cabral': '4'}}
    """
    def __process_output_layout(self, input_data: Layout) -> dict[str: str]:
        hashmap = dict[str: str]()

        measure_dimentions = self.__process_dimentions_of(Type.MEASURE, input_data)
        measured_dimentions = self.__process_dimentions_of(Type.MEASURED, input_data)
        measurer_dimentions = self.__process_dimentions_of(Type.MEASURER, input_data)

        hashmap.update({self.settings: {
            Type.MEASURE.name: {
                "col-span": measure_dimentions["col-span"],
                "row-span": measure_dimentions["row-span"]
            },
            Type.MEASURED.name: {
                "col-span": measured_dimentions["col-span"],
                "row-span": measured_dimentions["row-span"]
            },
            Type.MEASURER.name: {
                "col-span": measurer_dimentions["col-span"],
                "row-span": measurer_dimentions["row-span"]
            }
        }})

        hashmap.update({self.headers: [
            input_data.get_type(Type.MEASURER)[0]["label"],
            input_data.get_type(Type.MEASURED)[0]["label"],
        ]})

        hashmap.update({self.content: {}})
        content = hashmap[self.content]

        # iniciar hashmap com as labels dos measurers
        for question in input_data.get_type(Type.MEASURE):
            rows = question["rows"]
            hashmap[self.headers].append(question["label"])

            for row in rows:
                measurer_name = row["measurer"]
                measured_name = row["measured"]
                grade = row["grade"]

                if measurer_name not in content.keys():
                    content.update({measurer_name: {}})
                
                if measured_name not in content[measurer_name].keys():
                    content[measurer_name].update({measured_name: grade})

        hashmap[self.settings][Type.MEASURER.name]["row-span"] = len(hashmap.keys()) - 1
        print(hashmap)
        return []
    
    def __process_dimentions_of(self, type: Type, data: Layout) -> { "row-span": int, "col-span": int}:
        obj = data.get_type(type)

        if not obj:
            return {
                "row-span": 0,
                "col-span": 0
            }

        try:
            row_span = obj["row-span"] if obj["row-span"] else 1
            col_span = obj["col-span"] if obj["col-span"] else 1
        except:
            row_span = 1
            col_span = 1

        return {
            "row-span": row_span,
            "col-span": col_span
        }

    # treeData = [["Type", "Leaf Color", "Height"], ["Maple", "Red", 549], ["Oak", "Green", 783], ["Pine", "Green", 1204]]
    def __save_file(self, data, filepath):

        wb = Workbook()
        ws = wb.active

        settings = data[self.settings]
        headers = data[self.headers]
        content = data[self.content]

        # Definir o header
        ws.append(headers)

        # Measurer col-span
        wb.save(filepath)
    
    