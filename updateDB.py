from database.tools import Parser,Getter
from pathlib import Path
parser,getter =Parser(Path("./conf/local.ini").resolve()),Getter(Path("./conf/local.ini").resolve())
parser.insertResume()
subcats_collecitons=['basics','educations','projects','works','skills']
subcats_json_names=['basics','education','projects','work','skills']

for cats in zip(subcats_collecitons,subcats_json_names):
    getter.getCollection(cats[0]).delete_many({})
    parser.insertSubcat(cats[0],cats[1])
