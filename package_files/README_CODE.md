
```python
import automic_rest as automic


"""
 accessible response variables
    - url          # request url
    - body         # post body
    - headers      # response headers
    - status       # http status_code
    - content      # raw bytes
    - text         # content to string 
    - response     # content to json
"""

# init -  connection
# ----------------------------------------------------
automic.connection(
    url='https://automic-system-abc.de', 
    userid='user', 
    password='pass', 
    noproxy=True,       # defalut False 
    sslverify=False,    # default True
    timeout=60          # default 3600
)

# change connectio string (userid, password, url)
# ----------------------------------------------------
automic.connection(url="https://automic-system-xyz.de")
  
# help
# ----------------------------------------------------
# all modules
automic.help() 
# single module
automic.help(module="listAgents")

# listExecutions 
# ----------------------------------------------------
re = automic.listExecutions(client_id=1111)
for o in re.response['data']:
    print(o['name'])

# executeObject  -  ACTIVATE_UC_OBJECT
# ----------------------------------------------------
body = {
  "object_name": "SCRI.NEW.5",
  "execution_option": "execute",
  "inputs":
  {
    "PASS#": "test"
  }
 }

re = automic.executeObject(client_id=1111, body=body)
runid = re.response['run_id']
# getExecution
# ----------------------------------------------------
re = automic.getExecution(client_id=1111, run_id=runid)
print(re.response)

# wait until execution done
# ----------------------------------------------------
import time
def get_uc_status(client, runid):
    re = automic.getExecution(client_id=client, run_id=runid)
    return re.response['status']

while get_uc_status(1111, runid) != 1900:
    time.sleep(3)

# listReportContent 
# ----------------------------------------------------
re = automic.listReportContent(client_id=1111, run_id=runid, report_type='ACT')
print(re.response['data'][0]['content'])



# list Agents
# ----------------------------------------------------
re = automic.listAgents(client_id=1111)
if re.status == 200:
    for agent in re.response['data']:
        # do some stuff
        print(agent['name'])

# productList telemetry
# ----------------------------------------------------
re = automic.productList(client_id=1111)
print(re.text)

# usageObject
# ----------------------------------------------------
re = automic.usageObject(client_id=1111, object_name='EXY.EXAM.JOBS')
print(re.response)

# activateScript
# ----------------------------------------------------
re = automic.activateScript(client_id=1111, body={"script": ":SET &VAR# = 'PYTHON is ....' \n:PRINT &VAR#"})
runid = re.response['run_id']
re = automic.listReportContent(client_id=1111, run_id=runid, report_type='ACT')
print(re.response['data'][0]['content'])


```