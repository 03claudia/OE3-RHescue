
class File:
    file = None 
    page_name = "No name"
    config = {}
    file_index = 0

    def __str__(self):
        return f"File: {self.file},\n Page Name: {self.page_name},\n Config: {self.config},\n File Index: {self.file_index}"

