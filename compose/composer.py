import jinja2

from util.struct import Map
import configparser
from pathlib import Path
from database.tools import Getter
class Composer:

    def __init__(self,conf_pathgit):

        self.config = configparser.ConfigParser()
        read_done=self.config.read(Path(conf_path).resolve())

        self.latex_jinja_env = jinja2.Environment(
            block_start_string = '\BLOCK{',
            block_end_string = '}',
            variable_start_string = '\VAR{',
            variable_end_string = '}',
            comment_start_string = '\#{',
            comment_end_string = '}',
            line_statement_prefix = '%%',
            line_comment_prefix = '%#',
            trim_blocks = True,
            autoescape = False,
            loader=jinja2.FileSystemLoader(str(Path(self.config["DEFAULT"]["Template_dir"]).resolve()))
        )
        self.template = self.latex_jinja_env.get_template(self.config["DEFAULT"]["Base_template"])

        self.getter = Getter(Path(conf_path).resolve())
        self.resume_map =Map(self.getter.getResume(self.config["DEFAULT"]["Name"]))#resume_map is custom map
#write basic info
        self.basic_map = self.extracSocialProfile(Map(self.resume_map.basics))
        self.work_list = self.getter.getWorks()
        self.project_list = self.getter.getProjects()
        self.education_list = self.getter.getEducation()
        self.skill_list = self.getter.getSkills()
        self.tag_list = self.getter.getAllTags()
    def extracSocialProfile(self,basic_map):
        #basic_map is custom map
        for p in basic_map.profiles:
            name =p["network"]#name='github' p is dict
            basic_map[name] =Map({'url':p['url']})
            #basic_map[name].url = p["url"]
        return basic_map

    def updateProjectList(self,tags):
        self.project_list = self.getter.getProjects(tags)

    def selectList(self,target_list,sel_list):
        if sel_list==[]:
            return target_list
        else:
            return [target_list[i] for i in sel_list]

    def getTexPath(self):
        return str(Path(self.config['DEFAULT']['Output_dir'],'resume.tex').resolve())
    def getPdfPath(self):
        return str(Path(self.config['DEFAULT']['Output_dir'],'resume.pdf').resolve())
    def getOutputDir(self):
        return str(Path(self.config['DEFAULT']['Output_dir']).resolve())

    def generate(self,education_list,project_list,skill_list):

        output_str= self.template.render(resume= self.resume_map,
                                    basic = self.basic_map,
                                    works=self.work_list,
                                    projects=project_list,
                                    educations=education_list,
                                    skills=skill_list)


        with open(self.getTexPath(),'w') as out:
            out.write(output_str)
