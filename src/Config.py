import json
from Log.Logger import Logger

from Types import Type


class Config:
    data = {}
    layout = ""
    logger: Logger 

    """
        Caso, read_from_file seja True, o layout será lido do arquivo especificado em filepath.
        Daí, o layout passa a especificar o caminho para o ficheiro a ser lido, assumindo que é
        um ficheiro JSON.
    """

    def __init__(self, read_layout_from_file: bool, layout: str, logger: Logger = Logger("")) -> None:
        self.layout = layout
        self.logger = logger

        content = None
        if read_layout_from_file:
            content = json.loads(self.__read_layout_from_file())
        else:
            content = layout
        self.data = content
    

    def get_filename(self) -> str:
        return self.layout

    def get_data(self, type_used="layout"):
        return self.data[type_used]

    def get_data_as_json(self):
        return self.data
        self.logger.print_info(self.data)
        return json.dumps(self.data)

    def get_type(self, key: Type, data=None) -> list:
        if not data:
            data = self.get_data()
        result = []
        for row in data:
            if row["type"] == key.name:
                result.append(row)
            elif row["type"] == Type.CONTENT.name:
                result += self.get_type(key, row["rows"])

        return result

    # Enables us to edit the data directly
    def get_type_mut(self, key: Type, data=None) -> dict:
        if not data:
            data = self.get_data()
        for row in data:
            if row["type"] == key.name:
                return row
            elif row["type"] == Type.CONTENT.name:
                return self.get_type(key, row["rows"])

        return {} 

    def set_data_directly(self, data) -> None:
        self.data = data

    def __read_layout_from_file(self):
        try:
            with open(self.layout, "r", encoding='UTF-8') as file:
                return file.read()
        except FileNotFoundError:
            self.logger.print_error(f"Config file not found, reading: {self.layout}")
            exit(1)
        except Exception as e:
            self.logger.print_error(e)
            exit(1)

    def process_dimentions_of(
        self, type: Type, type_used="layout", max_span=0
    ) -> {"row-span": int, "col-span": int}:
        obj = (
            self.get_type(type)
            if type_used == "layout"
            else self.get_type(type, self.get_data(type_used))
        )

        if not obj:
            return {"row-span": 0, "col-span": 0}

        try:
            row_span = obj[0]["row-span"] if obj[0]["row-span"] else 1
        except:
            row_span = 1

        try:
            col_span = obj[0]["col-span"] if obj[0]["col-span"] else 1
        except:
            col_span = 1

        if row_span == "full":
            row_span = max_span
        if col_span == "full":
            col_span = max_span

        return {"row-span": row_span, "col-span": col_span}

    def leaf_iter(self, type_used="layout"):
        for row in self.data[type_used]:
            if row["type"] == Type.CONTENT.name:
                for leaf in row["rows"]:
                    yield leaf
            else:
                yield row
