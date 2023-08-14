import json

from Types import Type

class Layout:
    data = {}

    """
        Caso, read_from_file seja True, o layout será lido do arquivo especificado em filepath.
        Daí, o layout passa a especificar o caminho para o ficheiro a ser lido, assumindo que é
        um ficheiro JSON.
    """
    def __init__(self, read_layout_from_file: bool, layout: str, filepath: str) -> None:
        if not filepath and not layout:
            self.filepath = ""
            self.data = {}
            return
        self.layout = layout
        content = self.__read_layout_from_file() if read_layout_from_file else layout
        self.data = json.loads(content)
        self.filepath = filepath

    def get_data(self):
        return self.data["layout"]

    def get_filepath(self):
        return self.filepath
    
    def get_type(self, key: Type) -> list:
        result = []
        for row in self.get_data():
            if row["type"].lower() == key.name.lower():
                result.append(row)
            
        return result
    
    def set_data_directly(self, data) -> None:
        self.data = data
    
    def __read_layout_from_file(self):
        try:
            with open(self.layout, "r") as file:
                return file.read()
        except FileNotFoundError:
            print("File not found.")
            exit(1)
        except Exception as e:
            print(e)
            exit(1)

    
    