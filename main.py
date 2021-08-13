import json, re, os
from pprint import pprint
from urllib.request import urlopen
from shutil import copyfile



package_name = "automic_rest"
package_home = "c:\\Users\\xgadyou\\Entwicklung\\GITUB\\"+package_name  
package_path = package_home+"/"+package_name  
swagger_json = 'https://docs.automic.com/documentation/webhelp/english/AA/12.3/DOCU/12.3/REST%20API/Automation.Engine/swagger.json'



def get_path_params(path):
    output = []
    input = path.split('/')
    for p in input:
        if "{" in p:
            
            pt = p.replace('{', '').replace('}', '')
            if pt == "client_id" or pt == "run_id":
                pt = pt+ ":int=0"
            else:
                pt = pt+ "=None"

            if pt in output:
                output.append("target_"+p.replace('{', '').replace('}', '') + "=None")
            else:
                output.append(pt)
    return ', '.join(output)

def load_jsonfile(jsonfile):
    try:
        f = urlopen(jsonfile)
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
        copyfile(here+'/package_files/'+file, dst+'/'+file)
    
def copy_package_modules(dst):
    files = ["connection.py", "help.py"]
    here = os.path.abspath(os.path.dirname(__file__))
    for file in files:
        print("Copy {0} to package_dir".format(file))
        copyfile(here+'/package_files/'+file, dst+'/'+file)
    
    

# MAIN
create_folder(package_path)
copy_package_files(package_home)
copy_package_modules(package_path)
data = load_jsonfile(swagger_json)

  
# Iterating through the json
# Create a list for all moduless
list = []
modules = []
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
        
    for  method in data['paths'][i]:
        if 'operationId' in data['paths'][i][method]: 
            operationId = data['paths'][i][method]['operationId']
            
            if 'summary' in data['paths'][i][method]:
                summary = data['paths'][i][method]['summary']
            else:
                summary = ''

            has_query = False
            has_body = False
            if 'parameters' in data['paths'][i][method]:
                parameters = data['paths'][i][method]['parameters']
                c=0
                for el in parameters:
                    if 'schema' in el: 
                        parameters[c].pop('schema')
                    c +=1    
                    #if 'schema' in el: del parameters[el]['schema']
                for el in parameters:
                    if 'in' in el and el['in'] == 'query':
                        has_query = True
                        #if true get query and build it from vars
                        #print("-- " +operationId + ' has_query '+ el['name'])

                    if 'in' in el and el['in'] == 'body':
                        has_body = True
                        #if true get body
                        #print("-- " +operationId + ' has_body '+ el['name'])
                    # put query and body in help list
            else:
                parameters = ''

            res = any(ele.isupper() for ele in operationId)
            if res == False:
                if operationId != str_list[-1] and str_list[-1] != "merge":
                    operationId = operationId+str_list[-1].capitalize()
                elif operationId == "merge":
                    operationId = operationId+"Repository"
                elif operationId == "ping":
                    operationId = "ping"
                elif operationId == "usage":
                    operationId = "usageObject"
                else:
                    if str_list[-2] == "repositories":
                        operationId = operationId+"Repository"
                    else:
                        operationId = operationId+str_list[-2].capitalize()
             
            modules.append(operationId)

            print(module + ' ' + operationId + ' ' + method + ' ' + i)
            filename = operationId.lower()+'.py'
            fl = open(package_path+'/'+filename, "w")
      
            fl.write("import os\n")
            fl.write("import json\n") 
            fl.write("from automic_rest import config\n")
            fl.write("import requests\n")
            fl.write("from requests.exceptions import HTTPError\n")
            fl.write("from requests.exceptions import Timeout\n")           
            fl.write("from requests.packages.urllib3.exceptions import InsecureRequestWarning\n")
            fl.write("\n")
            fl.write("requests.packages.urllib3.disable_warnings(InsecureRequestWarning)\n")
            fl.write("\n\n")
            
            fl.write("\n\n")
            fl.write("class " + operationId + ":\n")
            
            if method == 'get':
                if operationId == "ping":
                    fl.write("   def __init__(self):\n")
                else:
                    if has_query:      
                        fl.write("   def __init__(self, "+get_path_params(i)+", query=None):\n")
                    else:
                        fl.write("   def __init__(self, "+get_path_params(i)+"):\n")
            else:
                if has_query:      
                    fl.write("   def __init__(self, "+get_path_params(i)+", body=None, query=None):\n")
                else:       
                    fl.write("   def __init__(self, "+get_path_params(i)+", body=None):\n")              
            
            fl.write("       # Summary: " + summary +"\n")
            fl.write("       self.response = None \n")
            fl.write("       self.body = None \n")
            fl.write("       self.url = None \n")
            fl.write("       self.headers = None \n")
            fl.write("       self.content = None \n")
            fl.write("       self.text = None \n")
            fl.write("       self.status = None \n")
            fl.write("       self.path = config().setArgs('"+i+"', locals())\n")
            if method == 'post':
                fl.write("       self.bodydata = body \n")
            if has_query:      
                fl.write("       if query != None:\n")
                fl.write("            self.query = '?'+query\n") 
                fl.write("       else:\n")
                fl.write("            self.query = ''\n")
                
            fl.write("\n")
            fl.write("       self.request() \n")
            fl.write("\n")
            fl.write("   def request(self): \n")
            #if method == 'post':
            fl.write("       requests_headers = {\n")
            fl.write("                              'Content-type': 'application/json', \n")
            fl.write("                              'Accept': 'application/json', \n")
            fl.write("                              'Authorization' : \"Basic %s\" % config().base64auth \n")
            fl.write("       }\n")
            fl.write("       try: \n")
            fl.write("            r = requests."+method+"(\n")
            if has_query:      
                fl.write("                config().url+self.path+self.query, \n")
            else:
                fl.write("                config().url+self.path, \n")
            fl.write("                headers=requests_headers,\n")
            if method == 'post':
                fl.write("                data=json.dumps(self.bodydata),\n")
            #fl.write("                auth=(config().userid, config().password), \n")
            fl.write("                verify=config().sslverify, \n")
            fl.write("                timeout=config().timeout \n")
            fl.write("            ) \n")
            if operationId != "ping":
                fl.write("            # request body  \n")
                fl.write("            self.body = r.request.body \n")
                fl.write("            # request url \n")
                fl.write("            self.url = r.request.url \n")
                fl.write("            # response headers \n")
                fl.write("            self.headers = r.headers \n")
                fl.write("            # raw bytes \n")
                fl.write("            self.content = r.content \n")
                fl.write("            # converts bytes to string \n")
                fl.write("            self.text = r.text \n")
                fl.write("            # convert raw bytes to json_dict \n") 
                fl.write("            self.response = r.json() \n")
                fl.write("            # http status_code \n")
            fl.write("            self.status = r.status_code \n")
            fl.write("            # If the response was successful, no Exception will be raised \n")
            fl.write("            r.raise_for_status() \n")
            fl.write("       except HTTPError as http_err: \n")
            fl.write("            print(f'HTTP error occurred: {http_err}')  # Python 3.6 \n")
            fl.write("       except Exception as err: \n")
            fl.write("            print(f'Other error occurred: {err}')  # Python 3.6 \n")
            fl.write("       except Timeout: \n")
            fl.write("            print('The request timed out') \n")
            fl.write("       else: \n")
            fl.write("            pass \n")
            fl.write(" \n")
            fl.write("       \n")
            fl.write("       return  self \n")

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

for mod in modules:
    f.write("from automic_rest."+mod.lower()+" import "+mod+" \n")

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
