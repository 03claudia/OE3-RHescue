from typing import Union
from Log.Logger import Logger
from Config import Config
import pandas as pd

class ExcelInterpretor:
    config: Config
    target_file: pd.DataFrame
    logger: Logger

    def __init__(self, config: Config, input_file: str, logger: Logger = Logger("")) -> None:
        self.logger = logger
        self.config = config
        self.target_file_name = input_file
        self.target_file = self.read_doc(input_file)

    def read_doc(self, input_file) -> pd.DataFrame:
        try:
            file = pd.read_excel(input_file)
            return file
        except FileNotFoundError:
            self.logger.print_critical_error(f"File not found: {input_file}")
            exit(1)
        except Exception:
            self.logger.print_critical_error(f"File {input_file} is not an excel")
            exit(1)

    def find_index_and_value_of_column(
        self, label: str
    ) -> Union[list[tuple[int, str]], tuple[int, str]]:
        label_to_find = label

        matching_columns = [
            col
            for col in self.target_file.columns
            if label_to_find.lower() in col.lower()
        ]

        result = []
        if matching_columns:
            for col_name in matching_columns:
                col_index = self.target_file.columns.get_loc(col_name)
                result.append((col_index, col_name))
        else:
            self.logger.print_critical_error(f"\nNo column matching label '{label_to_find}' found.")

        if len(result) == 1:
            return result[0]

        if len(result) == 0:
            return None

        return result

    def get_column_values(self, index: int) -> list:
        values = self.target_file.iloc[:, index].values.tolist()
        indexes = [i for i in range(len(values))]
        return list(zip(indexes, values))

    def get_config(self) -> Config:
        return self.config

    def get_target_file(self) -> pd.DataFrame:
        return self.target_file

    def get_target_file_name(self) -> str:
        return self.target_file_name
