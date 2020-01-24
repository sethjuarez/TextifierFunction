import os
import json
import logging
import requests
import azure.functions as func

absaEndpoint = os.environ["AbsaEndpoint"]
origins = os.environ["AllowOrigin"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info(f'Method: {req.method}')

    if req.method == "OPTIONS":
        logging.info(f'Handling OPTIONS query with allowed origin: {origins}')
        return func.HttpResponse(status_code=204,                             
                            headers={ 
                                'Access-Control-Allow-Headers': 'content-type',
                                'Access-Control-Allow-Methods': 'POST',
                                'Access-Control-Max-Age': '180',
                                'Access-Control-Allow-Origin': origins })


    body = req.get_json()
    text = body['text']
    logging.info(f'Querying {absaEndpoint} for [{text}]')
    response = {}
    try:
        resp = requests.post(absaEndpoint, json={ 'text': text })
        if resp.status_code == 200:
            logging.info(f'Response: {resp.content}')
            response = resp.json()
            response['error'] = {}
        else:
            logging.info(f'Request error: {resp.status_code}')
            response['error'] = {
                'code': resp.status_code,
                'message': resp.json(),
                'type': 'Request Error'
            }

    except Exception as error:
            logging.exception('Python Error')
            response['error'] = { 
                'code': '500',
                'message': f'{type(error).__name__}: {str(error)}',
                'type': 'Other Error'
            }

    return func.HttpResponse(body=json.dumps(response),
                                status_code=200,
                                headers={ 
                                    'Content-Type': 'application/json',
                                    'Access-Control-Allow-Origin': origins  })

