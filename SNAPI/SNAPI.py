import os
import requests

class SNREST(object):
    """docstring for SNREST. SNREST is a class meant for 
    interacting with the REST APIs of an instance of ServiceNow.
    """
    def __init__(self, **kwargs):
        super(SNREST, self).__init__()

        session = self.get_session(kwargs)

        environment = self.get_environment(kwargs)

        self.session = session
        self.environment = environment
        self.headers = {"Content-Type":"application/json","Accept":"application/json"}

    def __repr__(self): 
        """"""
        return f'<SNAPI interface ({self.environment})>'

    def get_environment(self, dictionary):
        environment = dictionary.pop("environment", False)
        if(not environment):
            environment = get_environment()
        return environment

    def get_session(self, dictionary):
        session = dictionary.pop("session", False)
        if(not session):
            session = requests.Session()
            session.auth = get_auth()
        return session

    def get_record(self, table, encoded_query):
        """"""
        url = f'https://{self.environment}.service-now.com/api/now/table/{table}'
        url = url + f'?sysparm_query={encoded_query}'

        response = self.session.get(url, headers=self.headers)
        
        if(not response.ok):
            raise requests.HTTPError(response=response)
        
        return response

    def create_record(self, table, payload):
        """"""
        url = f'https://{self.environment}.service-now.com/api/now/table/{table}'
        response = self.session.post(url, headers=self.headers, json=payload)
        return response
        
def get_auth():
    """function responsible for getting the username and password
    from the environment variables SN_USERNAME and SN_PASSWORD
    for interacting with the REST APIs of the SN_ENVIRONMENT.
    returns a tuple:(<username>, <password>)"""
    username = os.environ.get("SN_USERNAME", False)
    if(not username):
        raise RuntimeError("Environment Variable not found: <SN_USERNAME>")

    password = os.environ.get("SN_PASSWORD", False)
    if(not password):
        raise RuntimeError("Environment Variable not found: <SN_PASSWORD>")

    return (username, password)

def get_environment():
    """function responsible for getting the SN environment
    from the environment variable SN_ENVIRONMENT
    for interacting with the REST APIs of the SN_ENVIRONMENT instance.
    returns a string: <environment>"""
    environment = os.environ.get("SN_ENVIRONMENT", False)
    if(not environment):
        raise RuntimeError("Environment Variable not found: <SN_ENVIRONMENT>")

    return environment
