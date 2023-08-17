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

        for row in self.process_data_row(data):
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
                
    """
    [
        [ "Mariana", "Antonio", "6", "6" ],
        [ "Mariana", "Sofia", "6", "6" ],
        [ "Mariana", "Antonieta", "6", "6" ],
    ]
    """

    def process_data_row(self, data):
        rows = [[]]

        for item in data:
            rows[-1].append(item)

            if item["break-line"] == True:
                rows.append([])
        rows.pop()

        result = []
        major_data = None
        major_i = 0
        for row in rows:
            new_row = []
            row_spans = []

            if major_i < 0:
                major_data = None
                major_i = 0
        
            if row[0]["major"] == True:
                major_data = row[0]
                major_i = row[0]["major-span"]

            if major_data:
                for _ in range(major_data["col-span"]):
                    new_row.append(major_data)
            
            for item in row:
                if major_data != None and item == major_data:
                    continue

                for _ in range(item["col-span"]):
                    row_spans.append(item["row-span"])
                    new_row.append(item)
                
            for _ in range(max(row_spans)):
                result.append(new_row)

            major_i -= 1

        data_ready_to_draw = []
        for row in result:
            new_row = []
            for item in row:
                new_row.append(item["label"])
            data_ready_to_draw.append(new_row)

        print("\n\n", data_ready_to_draw)

        return data_ready_to_draw
            

            


    def __apply_style(self, ws, data:list[dict]):
        for style in data:
            ws.merge_cells(start_row=style['row-start'], start_column=style['col-start'],
                        end_row=style['row-end'], end_column=style['col-end'])
    
    def __apply_style_to_all_cells(self, ws, stylename, style):
        for row in ws.iter_rows():
            for cell in row:
                setattr(cell, stylename, style)

    

        

    