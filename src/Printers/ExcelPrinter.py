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
        data = self.__process_output_layout(self.layout)
        self.__save_file(data, filepath)
        
    def __process_output_layout(self, input_data: Layout) -> dict[str: str]:
        data = input_data.get_data()
        result = []

        for row in data:
            col_span = self.__get_property(row, "col-span", 1)
            row_span = self.__get_property(row, "row-span", 1)
            break_line = self.__get_property(row, "break-line", False)
            offset_col = self.__get_property(row, "offset-col", 0)

            self.__add_style_process(row, col_span, row_span, break_line, offset_col)

        return data

    def __get_property(self, row: dict, property: str, default_to):
        try:
            return row[property]
        except:
            return default_to

    def __add_style_process(self, row: dict, col_span, row_span, same_row: bool = False, offset_col = 0):
        row.update({
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

        

    def __save_file(self, data, filepath):
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, PatternFill

        wb = Workbook()
        ws = wb.active

        for row in self.draw(data):
            ws.append(row)
            
        self.__apply_style(ws, data)

        # Save the workbook
        wb.save(filepath)
    
    def draw(self, data):
        result = []
        for row, row_span in self.iter_get_line(data):
            for _ in range(row_span):
                result.append(row)
        return result
                

    def iter_get_line(self, data):
        row = []
        row_span_sizes = []
        max_row_size = 0

        for item in data:
            col_size = item['col-end'] - item['col-start'] + 1
            row_size = item['row-end'] - item['row-start'] + 1

            row_span_sizes.append(row_size)

            for _ in range(col_size):
                row.append(item['label'])

            if item['break-line']:
                max_row_size = max(row_span_sizes)
                yield row, max_row_size
                row = []
                row_span_sizes = []

    def __apply_style(self, ws, data:list[dict]):
        for style in data:
            ws.merge_cells(start_row=style['row-start'], start_column=style['col-start'],
                        end_row=style['row-end'], end_column=style['col-end'])
    
    def __apply_style_to_all_cells(self, ws, stylename, style):
        for row in ws.iter_rows():
            for cell in row:
                setattr(cell, stylename, style)

    

        

    