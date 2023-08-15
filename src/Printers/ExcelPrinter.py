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

    __process_col_pos = 0
    __process_row_pos = 0

    def __init__(self, layout: Layout):
        self.layout = layout

    def print(self, filepath):
        data, style = self.__process_output_layout(self.layout)
        self.__save_file(data, style, filepath)
        
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
    
    # Parte extremamente confusa e ainda cheia de bugs...
    def __final_processing_stage(self, hashmap: dict) -> list[list[str]]:
        final_output = []

        style = []

        settings = hashmap[self.settings]
        headers = hashmap[self.headers]
        content = hashmap[self.content]
        main_header = hashmap[self.main_headers]

        # Calculate column and row spans
        measurer_col_span = settings[Type.MEASURER.name]["col-span"]
        measured_col_span = settings[Type.MEASURED.name]["col-span"]
        measure_col_span = settings[Type.MEASURE.name]["col-span"]

        measured_row_span = settings[Type.MEASURED.name]["row-span"]
        header_row_span = settings[Type.HEADER.name]["row-span"]

        # Add main header
        main_header_row = [main_header[0]] * (measurer_col_span + measured_col_span + measure_col_span * len(headers[2:]))
        final_output.append(main_header_row)

        # Add main header style
        self.__add_style_process(style, Type.HEADER.name, measurer_col_span + measured_col_span + measure_col_span * len(headers[2:]), 1, False)

        # Add headers
        header_row = [headers[0]] * measurer_col_span + [headers[1]] * measured_col_span

        self.__add_style_process(style, "SUBHEADER", measurer_col_span, 1, True)
        self.__add_style_process(style, "SUBHEADER", measured_col_span, 1, True)

        for header in headers[2:]:
            header_row.extend([header] * measure_col_span)
            self.__add_style_process(style, "SUBHEADER", measure_col_span, 1, headers[-1] != header)
        
        final_output.append(header_row)

        number_of_measured = len(content[next(iter(content))].keys())

        measurer_content_row_span = number_of_measured * measured_row_span
        measure_content_row_span = measured_row_span
        measured_content_row_span = measured_row_span

        prev_count_cycles = -1
        count_cycles = 0
        
        # Esta é definitivamente a pior parte do codigo
        # peço desculpa 
        for measurer in content.keys():
            self.__add_style_process(style, Type.MEASURER.name, measurer_col_span, measurer_content_row_span, True)

            for measured in content[measurer].keys():
                row = [measurer] * measurer_col_span + [measured] * measured_col_span

                # tecnica para formatar bem avaliadores,
                # avaliados e avaliações
                offset_col = measurer_col_span 
                if prev_count_cycles != count_cycles:
                    offset_col = 0
                    prev_count_cycles = count_cycles

                self.__add_style_process(style, Type.MEASURED.name, measured_col_span, measured_content_row_span, True, offset_col)

                size_of_measures = len(content[measurer][measured])
       
                for i in range(0, size_of_measures):
                    grade = content[measurer][measured][i]
                    row.extend([grade] * measure_col_span)                    

                    self.__add_style_process(style, Type.MEASURE.name, measure_col_span, measure_content_row_span, i != size_of_measures - 1, offset_col)

                for _ in range(0, measured_row_span):
                    final_output.append(row)

            count_cycles += 1
                

        return final_output, style

    def __add_style_process(self, style: list[dict], type: str, col_span, row_span, same_row: bool = False, offset_col = 0):
        style.append({
            "type": type,
            "col-start": self.__process_col_pos + 1 + offset_col,
            "col-end": self.__process_col_pos + col_span + offset_col,
            "row-start": self.__process_row_pos + 1,
            "row-end": self.__process_row_pos + row_span,
        })

        if not same_row:
            self.__process_col_pos = 0
            self.__process_row_pos += row_span
        else:
            self.__process_col_pos += col_span

        

    def __save_file(self, data, style, filepath):
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, PatternFill

        wb = Workbook()
        ws = wb.active

        for row in data:
            ws.append(row)

        print(style)

        self.__apply_style(ws, style)

        # Save the workbook
        wb.save(filepath)
    
    def __apply_style(self, ws, styles:list[dict]):
        for style in styles:
            ws.merge_cells(start_row=style['row-start'], start_column=style['col-start'],
                        end_row=style['row-end'], end_column=style['col-end'])
    
    def __apply_style_to_all_cells(self, ws, stylename, style):
        for row in ws.iter_rows():
            for cell in row:
                setattr(cell, stylename, style)

    

        

    