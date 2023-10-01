from Log.Logger import Logger
import xlsxwriter

class Dropdown:
    workbook = None
    options: dict[str, str] = []
    dropdown_cell: str = ''
    logger: Logger = None

    # usado para saber que opção está ativa e assim
    # colocar nas celulas o valor associado a essa opção
    # ex: Se o Pedro estiver selecionado, mostramos a nota
    # atribuida ao Pedro
    formulas: dict[str, str] = {}

    def __init__(self, workbook: xlsxwriter.Workbook, options: list[str], dropdown_cell: str, logger: Logger = Logger("")):
        self.workbook = workbook
        for option in options:
            self.formulas[option] = ''
        self.dropdown_cell = dropdown_cell
        self.logger = logger

    def add_condition_to(self, option_name: str, value: str, pos: str):
        if not self.formulas[option_name]:
            self.logger.print_error("A opção " + option_name + " não foi adicionada ao dropdown")

        option = f"=IF({self.dropdown_cell}=\"{option_name}\", {value}, \"\")" 
        prev_option = self.formulas[option_name];

        if prev_option:
            self.formulas[option_name] = f"{prev_option} & {option}"
            return

        self.formulas[option_name] = option


    def print_to_excel(self):
        workbook = xlsxwriter.Workbook(self.workbook);
        worksheet = workbook.add_worksheet("resultados")

        # Create a dropdown in cell A1
        worksheet.data_validation('A1', {'validate': 'list',
                                        'source': self.options.keys() 
                                        })

        for option in self.formulas.keys():
            # self.options[option] dá me a posição da célula
            worksheet.write_formula(self.options[option], self.formulas[option])

        # Save the workbook
        workbook.close()
