import json


class Layout:
    # se o layout for inválido, o programa dá crash
    def __init__(self, layout: str, filepath: str) -> None:
        self.data = json.loads(layout)
        self.filepath = filepath

    def get_data(self):
        return self.data
    
    def get_path(self):
        return self.filepath