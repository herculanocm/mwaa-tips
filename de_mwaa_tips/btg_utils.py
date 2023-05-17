import urllib3
import json
from base64 import b64encode

def get_id_auth(url_authentication: str, client_id: str, client_secret: str, scope: str) -> dict:
    clientAndSecret = (client_id + ":" + client_secret).encode("utf-8")
    userAndPass = b64encode(clientAndSecret).decode()

    headers_authentication = {
        'Content-Type': 'application/json',
        'client_id': client_id,
        'Authorization': ('Basic %s' % userAndPass)
    }
    pload_authentication = {
        "grant_type": "client_credentials",
        "scope": scope
    }
    encoded_pload = json.dumps(pload_authentication).encode('utf-8')
    http = urllib3.PoolManager()
    resp = http.request('POST', url_authentication,
                        body=encoded_pload, headers=headers_authentication)
    result_auth = json.loads(resp.data.decode("utf-8"))
    

    return result_auth

def get_token_from_auth(result_auth: dict) -> str:
    return result_auth['access_token']

def get_nodes_pages(qtd_pages: int, qtd_nodes: int) -> dict:

    # Crie a lista com os elementos
    elements = list(range(1, qtd_pages + 1))

    # Determine o número de elementos em cada faixa
    num_elements = len(elements)
    elements_por_faixa, resto = divmod(num_elements, qtd_nodes)

    # Distribua os elementos nas faixas
    dict_nodes = []
    inicio = 0
    for i in range(qtd_nodes):
        tamanho = elements_por_faixa + (resto > 0)
        faixa = elements[inicio : inicio + tamanho]
        dict_nodes.append({'node': (i + 1), 'pages': faixa})
        inicio += tamanho
        resto -= 1

    return dict_nodes