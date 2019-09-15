#presents the options thru cli
import subprocess
def present_cmd(lst,func):
    #func is function to choose index to present
    for index,content in enumerate(lst):
        print(index,func(content))
from pathlib import Path
def compileTex(out_dir,texfile_path,pdf_path,preview=True):
    path = Path(pdf_path)
    if path.exists():
        path.unlink()
    subprocess.run(['pdflatex',texfile_path,'-output-directory='+out_dir])
    #subprocess.run(['pdflatex', texfile_path, ])

    if preview:
        subprocess.Popen([pdf_path], shell=True)

        # subprocess.run(['START', '""', pdf_path],shell=False)


