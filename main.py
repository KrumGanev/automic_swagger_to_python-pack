import json, re, os
from pprint import pprint
from urllib.request import urlopen
from shutil import copyfile


def load_jsonfile(jsonfile):
    try:
        f = urlopen(jsonfile)
        #here = os.path.abspath(os.path.dirname(__file__))
        #f = open(here+'/api.json')
        print("File swagger.json loaded ")
        return  json.load(f)
    except:
        print('File swagger.json not reachable')
        exit()
    finally:
        f.close()

def create_folder(f):
    try:
        os.makedirs(f+"/")    
        print("Directory " , f ,  "created ")
    except FileExistsError:
        print("Directory " , f ,  " already exists ")
        pass  

def copy_package_files(dst):
    files = ["LICENSE", "README.md", "setup.py"]
    here = os.path.abspath(os.path.dirname(__file__))
    for file in files:
        print("Copy {0} to package".format(file))
        copyfile(here+'/'+file, dst+'/'+file)
    
def copy_package_modules(dst):
    files = ["connection.py", "help.py"]
    here = os.path.abspath(os.path.dirname(__file__))
    for file in files:
        print("Copy {0} to package_dir".format(file))
        copyfile(here+'/package_files/'+file, dst+'/'+file)
    
    

package_name = "automic_rest"
package_home = "c:\\Users\\xgadyou\\Entwicklung\\YouDEV/python\\automic\\packages\\"+package_name  
package_path = package_home+"/"+package_name  
swagger_json = 'https://docs.automic.com/documentation/webhelp/english/AA/12.3/DOCU/12.3/REST%20API/Automation.Engine/swagger.json'

# MAIN
create_folder(package_path)
copy_package_files(package_home)
copy_package_modules(package_path)
data = load_jsonfile(swagger_json)

  
# Iterating through the json
# Create a list for all moduless
list = []
help_list = {}

fl = open(package_path+'/dummy', "w")
for i in data['paths']:
    #print(i.replace('{','').replace('}',''))
    p = i.replace('/{client_id}/', '')
    p = re.sub('/{.*}', '', p)
    p = re.sub('^/', '', p)
    str_list = p.split('/')
    module = str_list[0]
   
    if module not in list:
        fl.close()
        list.append(module)
        #print("--------- create py " + module+'#')
        filename = module+'.py'
        fl = open(package_path+'/'+filename, "w")
        fl.write("import os\n")
        fl.write("import json\n") 
        fl.write("from automic_rest import config\n")
        fl.write("import requests\n")
        fl.write("from requests.packages.urllib3.exceptions import InsecureRequestWarning\n")
        fl.write("\n")
        fl.write("requests.packages.urllib3.disable_warnings(InsecureRequestWarning)\n")
        fl.write("\n\n")
        fl.write("class " + module + ":\n")
        fl.write("   def __init__(self):\n")
        fl.write("       self.response = None\n")
        fl.write("\n")
        fl.write("   def json(self):\n")
        fl.write("       return  json.loads(self.response)\n")
        fl.write("\n")
        fl.write("   def text(self):\n")
        fl.write("       return  self.response\n")
        fl.write("\n")

    for  method in data['paths'][i]:
        if 'operationId' in data['paths'][i][method]: 
            operationId = data['paths'][i][method]['operationId']
            if 'summary' in data['paths'][i][method]:
                summary = data['paths'][i][method]['summary']
            else:
                summary = ''

            if 'parameters' in data['paths'][i][method]:
                parameters = data['paths'][i][method]['parameters']
                c=0
                for el in parameters:
                    if 'schema' in el: 
                        parameters[c].pop('schema')
                    c +=1    
                    #if 'schema' in el: del parameters[el]['schema']
            else:
                parameters = ''

            res = any(ele.isupper() for ele in operationId)
            if res == False:
                if operationId != str_list[-1] and str_list[-1] != "merge":
                    operationId = operationId+str_list[-1].capitalize()

            print(module + ' ' + operationId + ' ' + method + ' ' + i)
            fl.write("   def " + operationId + "(self, **kwargs):\n")
            fl.write("       # Summary: " + summary +"\n")
            if method == 'post':
                fl.write("       headers = {'Content-type': 'application/json', 'Accept': 'application/json'}\n")
                fl.write("       data = kwargs.get('data',\"{}\")\n")
            fl.write("       path = config().setArgs('"+i+"', **kwargs)\n")
            fl.write("       r = requests."+method+"(\n")
            fl.write("           config().url+path,\n")
            if method == 'post':
                fl.write("           headers=headers,\n")
                fl.write("           data=json.dumps(data),\n") 
            fl.write("           auth=(config().userid, config().password),\n")
            fl.write("           verify=config().sslverify\n")
            fl.write("       )\n")
            fl.write("\n")
            fl.write("       self.response = r.text\n")
            fl.write("       return self\n\n")
            if module not in help_list:
                help_list[module] = {}
            help_list[module][operationId] = {"path": i, "method": method, "summary": summary, "parameters": parameters}

fl.close()

# help.py
#####################
helpdict = json.dumps(help_list, indent=4, sort_keys=True)
helpdict = helpdict.replace('true', 'True').replace('false', 'False')
f = open(package_path+'/help.py', "a")
f.write("\nhelp_list = "+helpdict+"\n\n")
f.close()

# __init__.py
f = open(package_path+'/__init__.py', "w")
f.write("from automic_rest.connection import connection, config \n")
f.write("from automic_rest.help import help \n")

for mod in list:
    f.write("from automic_rest."+mod+" import "+mod+" \n")
f.close()


os.remove(package_path+'/dummy') 





# build package & upload
#python39 -m pip install --upgrade build
#python39 -m build
#python39 -m pip install --upgrade twine
#export CURL_CA_BUNDLE=""
#python39 -m twine upload --repository testpypi dist/*
#python39 -m twine upload --skip-existing dist/*
#

# local 
# python39 -m pip --use-feature=in-tree-build install .

# virtual
# python39 -m venv env
# pip install -e /c/Users/xgadyou/Entwicklung/YouDEV/python/automic/rest-api/
