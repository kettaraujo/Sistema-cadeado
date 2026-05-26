import requests
from decouple import config
from django.core.cache import cache


CACHE_KEY_LISTA_CADEADOS = "lista_cadeados_assetscontrol"
CACHE_TIMEOUT = 300  # 300 segundos = 5 minutos


def obter_lista_cadeados():
    """
    Busca a lista de cadeados.

    Primeiro tenta usar o cache local.
    Se não existir cache, chama a API e salva por 5 minutos.
    """

    lista_cadeados_cache = cache.get(CACHE_KEY_LISTA_CADEADOS)

    if lista_cadeados_cache is not None:
        return {
            "sucesso": True,
            "lista_cadeados": lista_cadeados_cache,
            "origem": "cache"
        }

    url = config('ASSETSCONTROL_URL')
    token = config('ASSETSCONTROL_TOKEN')

    payload = {
        "FTokenID": token,
        "FAction": "QueryAdminVehicleList"
    }

    response = requests.post(url, json=payload, timeout=20)
    response.raise_for_status()

    dados = response.json()

    lista_cadeados = dados.get("FObject", [])

    cache.set(CACHE_KEY_LISTA_CADEADOS, lista_cadeados, timeout=CACHE_TIMEOUT)

    return {
        "sucesso": True,
        "lista_cadeados": lista_cadeados,
        "origem": "api"
    }


def buscar_cadeado_por_id(id_cadeado):
    """
    Busca o cadeado pelo FAssetID.
    Usa cache de 5 minutos para evitar chamadas repetidas na API.
    """

    try:
        resultado_lista = obter_lista_cadeados()

        lista_cadeados = resultado_lista["lista_cadeados"]
        origem = resultado_lista["origem"]

        for cadeado in lista_cadeados:
            if str(cadeado.get("FAssetID")).strip() == str(id_cadeado).strip():
                return {
                    "encontrado": True,
                    "cadeado": cadeado,
                    "mensagem": f"Cadeado encontrado. Fonte dos dados: {origem}."
                }

        return {
            "encontrado": False,
            "cadeado": None,
            "mensagem": f"Cadeado não encontrado. Fonte dos dados: {origem}."
        }

    except requests.exceptions.RequestException as erro:
        return {
            "encontrado": False,
            "cadeado": None,
            "mensagem": f"Erro ao consultar a API: {erro}"
        }


def abrir_cadeado_por_guid(asset_guid):
    """
    Envia para a API o comando de abertura do cadeado usando o FAssetGUID.

    Essa função não usa cache.
    Ela apenas recebe o FAssetGUID encontrado na busca e envia o comando.
    """

    url = config('ASSETSCONTROL_INSTRUCTION_URL')
    token = config('ASSETSCONTROL_TOKEN')

    payload = {
        "FTokenID": token,
        "FAction": "OpenLockControl",
        "FAssetGUID": asset_guid
    }

    try:
        response = requests.post(url, json=payload, timeout=20)
        response.raise_for_status()

        dados = response.json()

        result = dados.get("Result")
        message = dados.get("Message", "Sem mensagem retornada pela API.")

        if result == 200 or result == 0:
            return {
                "sucesso": True,
                "mensagem": "Comando de abertura enviado com sucesso para o cadeado."
            }

        if result == 111:
            return {
                "sucesso": False,
                "mensagem": "O cadeado foi encontrado, mas está offline. O comando não pôde ser executado."
            }

        return {
            "sucesso": False,
            "mensagem": f"A API recebeu o comando, mas retornou erro: {message}"
        }

    except requests.exceptions.RequestException as erro:
        return {
            "sucesso": False,
            "mensagem": f"Erro ao enviar comando de abertura: {erro}"
        }