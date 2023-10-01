from Config import Config
import Stategies.ResultStrategy.DropDown as Dropdown

# CUIDADO COM OS NOMES DOS FICHEIROS
class Results:

    data: list['Group']
    def __init__(self, data: list['Group']) -> Config:
        # todo
        self.data = data
        self.dropdown = Dropdown()


    # nome do excel tem de comecar com "gen_m"
    def process_av_des_mensal(self):
        pass

    # nome do excel tem de comecar com "gen_s"
    def process_av_des_sem(self):
        pass

    # nome do excel tem de comecar com "mem_proj_<nome do projeto>"
    def process_av_sem_mem_proj(self):
        pass

    # nome do excel tem de comecar com "pm_proj_<nome do projeto>"
    def process_av_sem_pm_proj(self):
        pass
        
    # nome do excel tem de comecar com "coord_proj_<nome do projeto>"
    def process_av_sem_coord_proj(self):
        pass
