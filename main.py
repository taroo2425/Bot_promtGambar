import json
import time
from config import API_KEY, API_SECRET  
import base64
import requests


class FusionBrainAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)


if __name__ == '__main__':
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API_KEY , API_SECRET)
    pipeline_id = api.get_pipeline()
    uuid = api.generate("rainy day at garden", pipeline_id)
    files = api.check_generation(uuid)
    print(files)

    encoded_string = files[0]
    decoded_data = base64.b64decode(encoded_string)

    with open("hujan.jpeg", "wb") as f:
        f.write(decoded_data)

#API_SECRET = "C7F356BF62F7135D0C10FE5D2FEAC48B"
#API_KEY = "DAAEEA222AE3AA35027865108386E15F"    