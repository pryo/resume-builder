try:
    import tkinter as tk
except:
    import Tkinter as tk
import pygubu

class View:
    def __init__(self, ui_file_path):
        self.builder = pygubu.Builder()

        # 2: Load an ui file
        self.builder.add_from_file(ui_file_path)

        # 3: Create the toplevel widget.

        self.main_window = self.builder.get_object('toplevel')
        self.education_lst = self.builder.get_object('education_lst')
        self.project_lst = self.builder.get_object('project_lst')
        self.skills_lst = self.builder.get_object('skills_lst')
        #self.tag_entry = self.builder.get_object('tag_entry')
        self.generate_btn = self.builder.get_object('generate_btn')
        self.tags_lst = self.builder.get_object('tags_lst')
