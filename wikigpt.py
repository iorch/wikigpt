import os
import requests
import json


openai_api_key = os.getenv("OPENAI_API_KEY")

def get_wiki_sm():
    uri = 'https://es.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=Modelo_est%C3%A1ndar_de_la_f%C3%ADsica_de_part%C3%ADculas'
    r = requests.get( uri )
    return r.text

def get_wiki_higgs():
    uri = 'https://es.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=Mecanismo_de_Higgs'
    r = requests.get( uri )
    return r.text

def get_wiki_feynman_diagram():
    uri = 'https://es.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=Diagrama_de_feynman'
    r = requests.get( uri )
    return r.text

def get_function_description():
    return [
        {
            "name": "get_wiki_sm",
            "description": "Get Wikipedia webpage of Standard Model of particle physics",
            "parameters": {
                "type": "object",
                "properties": {}
            },
        },
        {
            "name": "get_wiki_higgs",
            "description": "Get Wikipedia webpage of Higgs mechanism",
            "parameters": {
                "type": "object",
                "properties": {}
            },
        },
        {
            "name": "get_wiki_feynman_diagram",
            "description": "Get Wikipedia webpage of Feynman diagrams",
            "parameters": {
                "type": "object",
                "properties": {}
            },
        }
    ]


def get_wikiGPT():
    uri = 'https://api.openai.com/v1/chat/completions'

    function_description = get_function_description()

    data = {
        'model': 'gpt-3.5-turbo-16k',
        'messages': [
            {
                'role': 'system',
                'content': (
                    'You are an agent expert on particle physics. You MUST always answer in LATAM Spanish.'
                    'You are answering to physicist, and physics students in Mexico.'
                    'You have access to Wikipedia through function calls'
                ) 
            },
            {
                'role': 'user',
                'content': (
                    'Explicame el modelo estándard de física de partículas.'
                )
            }
        ],
        'functions': function_description,
        'function_call': 'auto'
    }
    payload = json.dumps(data)
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {openai_api_token}'.format(openai_api_token=openai_api_key),
    }

    r = requests.post(
        uri,
        headers = headers,
        data = payload
    )

    response = json.loads(r.text)
    response_message = response['choices'][0]['message']
    print(response)
    if response_message and response_message['function_call']:
        available_functions = {
            'get_wiki_sm': lambda: ( str( get_wiki_sm() ) ),
            'get_wiki_higgs': lambda: ( str( get_wiki_higgs() ) ),
            'get_wiki_feynman_diagram': lambda: ( str( get_wiki_feynman_diagram() ) ),
        }
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions.get(function_name)
        if function_to_call:
            function_response = function_to_call()
        else:
            function_response = "Not Known"

    (data['messages']).append(
        {
            "role": "function",
            "name": function_name,
            "content": function_response,
        }
    )
    payload = json.dumps(data)
    print(payload)
    r = requests.post(
        uri,
        headers = headers,
        data = payload
    )

    return r.text


if __name__ == "__main__":
    wiki_response = get_wikiGPT()
    print(wiki_response)

