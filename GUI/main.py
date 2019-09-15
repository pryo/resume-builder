
import os
from util.command import *
try:
    import tkinter as tk
except:
    import Tkinter as tk


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

from GUI.view import View
from compose.composer import Composer
class Application:
    def __init__(self,conf_path):
        # 1: Create a builder
        self.view = View(os.path.join(CURRENT_DIR, 'view.ui'))
        # self.builder = pygubu.Builder()
        #
        # # 2: Load an ui file
        # self.builder.add_from_file(os.path.join(CURRENT_DIR, 'view.ui'))
        #
        # # 3: Create the toplevel widget.
        # self.mainwindow = self.builder.get_object('toplevel')
        self.composer = Composer(conf_path=conf_path)
        self.view.builder.connect_callbacks(self)

        # self.view.tag_entry.bind('<Return>', self.changed_entry)
        self.loadListBox(self.composer.education_list,
                         self.view.education_lst,
                         lambda education:education['area']+','+education['institution'])
        self.loadListBox(self.composer.project_list,
                         self.view.project_lst,
                         lambda project: project['name'])
        self.loadListBox(self.composer.skill_list,
                         self.view.skills_lst,
                         lambda skill: skill['name'])
        self.loadListBox(self.composer.tag_list,
                         self.view.tags_lst,
                         lambda tag: tag)
        self.view.tags_lst.bind('<<ListboxSelect>>',self.changed_tag)
    def loadListBox(self,array,listBox_widget,func):
        listBox_widget.delete(0, tk.END)
        for item in array:
            listBox_widget.insert(tk.END,func(item))

    def quit(self, event=None):
        self.view.main_window.quit()

    def run(self):
        self.view.main_window.mainloop()

    def changed_entry(self,event):
        input =self.view.tag_entry.get()
        tag_lst =input.replace("\n","").split(',')
        self.composer.updateProjectList(tag_lst)
        self.loadListBox(self.composer.project_list,
                         self.view.project_lst,
                         lambda project: project['name'])
    def changed_tag(self,event):
        ind_lst = self.view.tags_lst.curselection()
        self.composer.updateProjectList([self.composer.tag_list[i] for i in ind_lst])
        self.loadListBox(self.composer.project_list,
                         self.view.project_lst,
                         lambda project: project['name'])



    def generate(self):
        edu_list=self.composer.selectList(self.composer.education_list,self.view.education_lst.curselection())
        proj_list=self.composer.selectList(self.composer.project_list, self.view.project_lst.curselection())
        skill_list=self.composer.selectList(self.composer.skill_list, self.view.skills_lst.curselection())
        self.composer.generate(edu_list,proj_list,skill_list)
        compileTex(self.composer.getOutputDir(),self.composer.getTexPath(),self.composer.getPdfPath())

# if __name__ == '__main__':
#     app = Application()
#     app.run()

