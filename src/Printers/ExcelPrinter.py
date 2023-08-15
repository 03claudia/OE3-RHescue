from typing import Union
from openpyxl import Workbook

import pandas as pd
from Layout import Layout
from Types import Type


class ExcelPrinter:
    settings = "_settings"
    headers = "_headers"
    content = "_content"
    main_headers = "_main_headers"

    def __init__(self, layout: Layout):
        self.layout = layout

    def print(self, filepath):
        data: list[list[str]] = self.__process_output_layout(self.layout)
        self.__save_file(data, filepath)
        
    def __process_output_layout(self, input_data: Layout) -> dict[str: str]:
        hashmap = dict[str: str]()

        measure_dimentions = self.layout.process_dimentions_of(Type.MEASURE)
        measured_dimentions = self.layout.process_dimentions_of(Type.MEASURED)
        measurer_dimentions = self.layout.process_dimentions_of(Type.MEASURER)
        header_dimentions = self.layout.process_dimentions_of(Type.HEADER)

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
            },
            Type.HEADER.name: {
                "col-span": header_dimentions["col-span"],
                "row-span": header_dimentions["row-span"]
            }
        }})

        hashmap.update({self.main_headers: [
            input_data.get_type(Type.HEADER)[0]["label"],
        ]})

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
                    content[measurer_name].update({measured_name: []})

                content[measurer_name][measured_name].append(grade)

        hashmap[self.settings][Type.MEASURER.name]["row-span"] = len(hashmap.keys()) - 1

        # Fazer com que o output fique o mais pronto possivel
        # para depois ser utilizado pelo openpyxl
        return self.__final_processing_stage(hashmap)
    
    def __final_processing_stage(self, hashmap: dict) -> list[list[str]]:
        final_output = []

        """ 
            "col-start": 0,
            "col-end": 0,
            "row-start": 0,
            "row-end": 0, 
        """
        style = []

        settings = hashmap[self.settings]
        headers = hashmap[self.headers]
        content = hashmap[self.content]
        main_header = hashmap[self.main_headers]

        # content
        measurer_col_span = settings[Type.MEASURER.name]["col-span"]
        measured_col_span = settings[Type.MEASURED.name]["col-span"]
        measure_col_span = settings[Type.MEASURE.name]["col-span"]

        measured_row_span = settings[Type.MEASURED.name]["row-span"]
        header_row_span = settings[Type.HEADER.name]["row-span"]

        row_size = 0

        # main header
        for _ in range(measurer_col_span):
            row = []
            for _ in range(measurer_col_span + measured_col_span + (measure_col_span * len(headers[2:]))):
                row.append(main_header[0])

            for _ in range(header_row_span):
                final_output.append(row)
            
        style.append({
            "type": Type.HEADER.name,
            "col-start": 0,
            "col-end": measurer_col_span + measured_col_span + (measure_col_span * len(headers[2:])),
            "row-start": size,
            "row-end": size + header_row_span,
        })
        size += header_row_span

        # headers
        for _ in range(measurer_col_span):
            row = []
            for _ in range(measurer_col_span):
                    row.append(headers[0])
            for _ in range(measured_col_span):
                    row.append(headers[1])
            for _ in range(measure_col_span):
                for header in headers[2:]:
                    row.append(header)

            final_output.append(row)
        
        col_size = 0
        style.append({
            "type": "SUB_HEADER",
            "col-start": col_size,
            "col-end": col_size + measurer_col_span,
            "row-start": size,
            "row-end": size + measured_row_span,
        })

        col_size += measurer_col_span
        style.append({
            "type": "SUB_HEADER",
            "col-start": col_size,
            "col-end": col_size + measure_col_span,
            "row-start": size,
            "row-end": size + measured_row_span,
        })

        col_size += measure_col_span
        for _ in range(len(headers[2:])):
            style.append({
                "type": "SUB_HEADER",
                "col-start": col_size,
                "col-end": col_size + measure_col_span,
                "row-start": size,
                "row-end": size + measured_row_span,
            })
            col_size += measure_col_span

        size += measured_row_span

        for measurer in content.keys():
            for measured in content[measurer].keys():
                row = []
                for _ in range(measurer_col_span):
                    row.append(measurer)

                style.append({
                    "type": Type.MEASURER.name,
                    "col-start": 0,
                    "col-end": measurer_col_span,
                    "row-start": size,
                    "row-end": size + measured_row_span,
                })
                
                for _ in range(measured_col_span):
                    row.append(measured)

                style.append({
                    "type": Type.MEASURED.name,
                    "col-start": measurer_col_span,
                    "col-end": measurer_col_span + measured_col_span,
                    "row-start": size,
                    "row-end": size + measured_row_span,
                })

                for _ in range(measure_col_span):
                    row += content[measurer][measured]

                style.append({
                    "type": Type.MEASURE.name,
                    "col-start": measurer_col_span + measured_col_span,
                    "col-end": measurer_col_span + measured_col_span + (measure_col_span * len(headers[2:])),
                    "row-start": size,
                    "row-end": size + measured_row_span,
                })

                for _ in range(measured_row_span):
                    final_output.append(row)
            
            size += measured_row_span
        
        # save the style
        final_output.append(style)

        return final_output

    def __save_file(self, data, filepath):
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, PatternFill

        wb = Workbook()
        ws = wb.active

        for row in data:
            ws.append(row)

        print(data[:-1])

        self.__apply_style(ws, data[:-1])

        # Save the workbook
        wb.save(filepath)
    
    def __apply_style(self, ws, styles):
        from openpyxl.styles import Alignment, PatternFill, Border, Side

        line = Side(border_style="thin", color="000000")
        borders = Border(left=line, right=line, top=line, bottom=line)
        self.__apply_style_to_all_cells(ws, "border", borders)
    
    def __apply_style_to_all_cells(self, ws, stylename, style):
        for row in ws.iter_rows():
            for cell in row:
                setattr(cell, stylename, style)

        

    