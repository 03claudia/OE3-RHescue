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
        data = input_data.get_data()
        result = []

        for row in data:
            col_span = row["col-span"] if row["col-span"] else 1
            row_span = row["row-span"] if row["row-span"] else 1
            break_line = row["break-line"] if row["break-line"] else False
            offset_col = row["offset-col"] if row["offset-col"] else 0

            self.__add_style_process(row, col_span, row_span, break_line, offset_col)

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

    

        

    