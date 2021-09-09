



from azureml.core import Webservice
for webservice in Webservice.list(ws):
    print('name:', webservice.name)
    if "manymodels" in webservice.name:
        Webservice(ws, name = webservice.name).delete()