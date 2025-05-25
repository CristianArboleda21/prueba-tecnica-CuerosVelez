import requests, os

def api_vtx(url, timeout=None):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'VtexIdclientAutCookie' : os.environ['TOKEN']
        }
        if timeout is not None:
            resp = requests.get(url, headers=headers, timeout=timeout)

        resp = requests.get(url, headers=headers)
        
        return resp.json()
    except:
        return "Error"