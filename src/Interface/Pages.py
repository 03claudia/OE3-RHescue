from Interface.File import File
import streamlit as st
import os

class Pages:
    def create_page(file: File):
        try:
            print(f"file.page_name: {file.page_name}")
            if file.page_name in os.listdir("./src/pages"):
                st.error(f"File {file.page_name} already exists.")
            else:
                with open(f"./src/pages/{file.page_name}.py", "w") as f:
                    f.write(f"import Interface.Interface as Interface\n")
                    f.write(f"import streamlit as st\n")
                    f.write(f"\n")
                    f.write(f"saved_files = st.session_state.saved_files\n")
                    f.write(f"st.write(\"{file.page_name}\")\n")
                    f.write(f"Interface.ler_ficheiro(saved_files[{file.file_index}])\n")
                st.write(f"File {file.page_name} created successfully.")
                st.session_state.new_file = None
        except Exception as e:
            st.error(f"An error occurred: {e}")

    def delete_page(file: File):

        pass
    
    def save_app_state(saved_files, filename="saved_files.txt"):
        with open(filename, "w") as f:
            for file in saved_files:
                aux = file.file.__str__().replace("\n", " ") if file.file else file.file
                f.write(f"{file.page_name}||,{file.file_index}||,{aux}||,{file.config}\n")

    def load_app_state(filename="saved_files.txt") -> list[File]:
        saved_files = []
        try:
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    for line in f:
                        page_name, file_index, file_name, config = line.strip().split('||,')
                        file = File()
                        file.page_name = page_name
                        file.file_index = int(file_index)
                        file.file_name = file_name
                        file.config = config
                        print("reading:", file.__dict__)
                        saved_files.append(file)
        except Exception as e:
            print(f"Error loading app state: {e}")
    
        return saved_files
