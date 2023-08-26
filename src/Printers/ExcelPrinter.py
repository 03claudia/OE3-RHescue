from typing import Union
from openpyxl import Workbook

import pandas as pd
from Config import Config
from Stategies.AvalStrat.StyleBinder import StyleBinder
from Types import Style, Type


class ExcelPrinter:
    settings = "_settings"
    headers = "_headers"
    content = "_content"
    main_headers = "_main_headers"

    __process_col_pos = 0
    __process_row_pos = 0
    
    def __init__(self, layout: Config):
        self.layout = layout

    def print(self, filepath):
        data = self.layout.get_data()
        self.__save_file(data, filepath)
        
    def __process_output_style(self, data: []) -> dict[str: str]:
 
        for row in data:
            col_span = row[Style.COL_SPAN.value[0]]
            row_span = row[Style.ROW_SPAN.value[0]]
            break_line = row[Style.BREAK_LINE.value[0]]
            offset_col = row["offset-col"] 
            major = row[Style.MAJOR.value[0]]

            self.__add_style_process(row, col_span, row_span, not break_line, offset_col, major)

        return data

    def __get_property(self, row: dict, property: str, default_to):
        try:
            return row[property]
        except:
            return default_to

    same_row = False
    def __add_style_process(self, row: dict, col_span, row_span, same_row: bool = False, offset_col = 0, major = False):
        row.update({
            "col-start": self.__process_col_pos + 1 + offset_col,
            "col-end": self.__process_col_pos + col_span + offset_col,
            "row-start": self.__process_row_pos + 1,
            "row-end": self.__process_row_pos + row_span,
        })

        if not same_row:
            self.__process_col_pos = 0
            self.__process_row_pos += row_span if not major else 1
        else:
            self.__process_col_pos += col_span + offset_col

        

    def __save_file(self, data, filepath):
        from openpyxl import Workbook, load_workbook
        from openpyxl.styles import Alignment, PatternFill

        # Primeira parte responsável por colocar e criar os dados
        # no arquivo excel
        writer = pd.ExcelWriter(filepath)
        
        num_cols = data[-1]["num-columns"]
        data_processed = self.process_data(data, num_cols)
        
        dict_data = {}

        random = 0
        for col in data_processed:
            try:
                dict_data.update({random: col})
                random += 1
            except:
                continue
        
        pdDataframe = pd.DataFrame(dict_data)
        pdDataframe.to_excel(writer, index=False, header=False, sheet_name="Sheet1")
        writer.close()

        # Segundo passo, voltar a abrir o arquivo e aplicar os estilos
        wb = load_workbook(filepath)
        ws = wb.active

        self.__apply_style(ws, data[:-1])

        # Save the workbook
        wb.save(filepath)

    def process_data(self, data, num_cols):
        cols = [[] for _ in range(num_cols)]
        index = 0

        for item in data:
            try:
                col_span = item["col-span"]
                row_span = item["row-span"]
                label = item["label"]
            except KeyError:
                continue

            for i in range(col_span):
                for _ in range(row_span):
                    try:
                        cols[index + i].append(label)
                    except:
                        print(f"Erro: {index + i}, provavelmente existe algo de errado com o layout ou com o excel de input.\
                              De qualquer das formas peço já desculpa por não ter detetado este erro antes.")

            index += col_span

            if index >= num_cols:
                index = 0

        return cols
    
    def __apply_style(self, ws, data:list[dict]):
        from openpyxl.styles import Alignment, PatternFill, Font, Border, Side

        major_data: dict[str: int] = {}
        style_list = []

        prev_item = None
        for style in data:

            if style[Style.MAJOR.value[0]] and style[Style.ID.value[0]] in major_data:
                item = major_data[style[Style.ID.value[0]]]

                if style[Style.BREAK_LINE.value[0]]:
                    if prev_item:
                        prev_item[Style.BREAK_LINE.value[0]] = True

                if item == 0:
                    del item

                item -= 1
                continue

            elif style[Style.MAJOR.value[0]]:
                major_data.update({
                    style[Style.ID.value[0]]: style[Style.MAJOR_SPAN.value[0]]
                })
                style["row-span"] = style[Style.MAJOR_SPAN.value[0]]

            style_list.append(style)
            prev_item = style

        self.__process_output_style(style_list)

        for style in style_list:
            ws.merge_cells(start_row=style['row-start'], start_column=style['col-start'],
                        end_row=style['row-end'], end_column=style['col-end'])
            
            alignment = Alignment(horizontal=style['x-alignment'], vertical=style["y-alignment"])
            font = Font(color=style['text-color'])
            fill = PatternFill(patternType='solid', fill_type='solid', fgColor=style['bg-color'])
            border = Border(
                left=Side(style=style["border"], color=style["border-color"], border_style=None),   # Black thin border
                right=Side(style=style["border"], color=style["border-color"], border_style=None),
                top=Side(style=style["border"], color=style["border-color"], border_style=None),
                bottom=Side(style=style["border"], color=style["border-color"], border_style=None)
            )

            self.__apply_style_to_cell(ws, style['row-start'], style['col-start'], 'alignment', alignment)
            self.__apply_style_to_cell(ws, style['row-start'], style['col-start'], 'fill', fill)
            self.__apply_style_to_cell(ws, style['row-start'], style['col-start'], 'font', font)

            for i in range(style['col-start'], style['col-end'] + 1):
                self.__apply_style_to_cell(ws, style['row-start'], i, 'border', border)
            
            for j in range(style['row-start'], style['row-end'] + 1):
                self.__apply_style_to_cell(ws, j, style['col-start'], 'border', border)
            
    def __apply_style_to_cell(self, ws, row, col, stylename, style):
        cell = ws.cell(row=row, column=col)
        setattr(cell, stylename, style)
    
    def __apply_style_to_all_cells(self, ws, stylename, style):
        for row in ws.iter_rows():
            for cell in row:
                setattr(cell, stylename, style)


    
