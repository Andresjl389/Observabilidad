import requests
import time
from sqlalchemy.orm import Session
from repositories.token_repository import get_by_id


def adpex(db: Session):
    token = get_by_id(db, '60e4daec-19f7-4cc7-a5fa-74c23cad2bf7')
    url = 'https://esd62814.live.dynatrace.com/api/v2/metrics/query'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Api-Token {token.token}'
    }
    params = {
        'metricSelector': '(builtin:apps.other.apdex.osAndVersion:filter(and(or(in("dt.entity.device_application",entitySelector("type(mobile_application),entityName.equals(~"SuperApp~")"))))):splitBy():sort(value(auto,descending)):limit(100)):limit(100):names',
        'from': '-h',
        'to': 'now',
        'resolution': 'Inf',
        'mzSelector': 'mzId(6734853283526883009)'
    }
    response = requests.get(url=url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}


def create_token(db: Session):
    url = 'https://sso.dynatrace.com/sso/oauth2/token'
    token = get_by_id(db, 'c052574a-9e1f-46cf-9d6e-6f87d2138c23')
    body = {
        'client_id': 'dt0s02.KLELLC3E',
        'grant_type': 'client_credentials',
        'client_secret': f'{token.token}',
        'resource': 'urn:dtaccount:5d8555d6-ac2e-4fca-82dd-d32e718916c4'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'AWSALB=7od9vDqM6B53dgMX3g5iWINGXnM2/uBdda5Hd8c9YPa0du/ox9ng5mDl0+D+x7siAW1gCfAH55oUGWIw5ePaMOhObRg4ei9s5DgfrTV+SmbLN+wkBkPu/yeP82JL; AWSALBCORS=7od9vDqM6B53dgMX3g5iWINGXnM2/uBdda5Hd8c9YPa0du/ox9ng5mDl0+D+x7siAW1gCfAH55oUGWIw5ePaMOhObRg4ei9s5DgfrTV+SmbLN+wkBkPu/yeP82JL'
    }
    response = requests.post(url=url, data=body, headers=headers)
    return response.json()['access_token']


def query(db: Session):
    token = create_token(db)
    url = 'https://esd62814.apps.dynatrace.com/platform/storage/query/v1/query:execute'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    body = {
        'timezone': 'America/Bogota',
        'query': 'fetch bizevents, from: now()-1h, to: now() '
        '\n|filter dt.system.bucket == \"bck-pn\"'
        '\n|filter dt.security_context == \"superapp_login_AuthenticationController_clientHello\"'
        '\n|fields userAgent, idData\n|filter isNotNull(userAgent) and isNotNull(idData)'
        '\n|summarize Cedulas_unicas = countDistinctApprox(idData)'
        '\n|append[fetch bizevents\n|filter dt.system.bucket == \"bck-pn\"'
        '\n|filter dt.security_context == \"superapp_login_SessionManagerController_getSession\"'
        '\n|filter isNotNull(idData)\n|summarize Total_Clientes_Autenticados = countDistinctApprox(idData)]'
        '\n| summarize Cedulas_unicas = sum(Cedulas_unicas), Total_Clientes_Autenticados = sum(Total_Clientes_Autenticados)'
        '\n|fieldsAdd pct = (Total_Clientes_Autenticados*100)/Cedulas_unicas'
        '\n|fields pct'
    }
    response = requests.post(url=url, json=body, headers=headers)
    return response.json()['requestToken']


def data():
    token = create_token()
    url = 'https://esd62814.apps.dynatrace.com/platform/storage/query/v1/query:poll'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    request_token = query()
    print(f"🔎 Request token: {request_token}")

    body = {
        'request-token': request_token
    }

    for attempt in range(10):
        response = requests.get(url=url, params=body, headers=headers)
        print(f"📡 Attempt {attempt+1}, status code: {response.status_code}")

        if response.status_code == 410:
            print("⚠️ Token expirado o recurso no disponible")
            return {"error": 410, "message": "El request-token ya no está disponible"}


def data(db: Session):
    token = create_token(db)
    url = 'https://esd62814.apps.dynatrace.com/platform/storage/query/v1/query:poll'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    request_token = query(db)
    print(f"🔎 Request token: {request_token}")

    body = {
        'request-token': request_token
    }

    for attempt in range(10):
        response = requests.get(url=url, params=body, headers=headers)

        try:
            result = response.json()
        except requests.exceptions.JSONDecodeError:
            return {"error": "Invalid JSON", "body": response.text}

        state = result.get("state")
        print(f"⏳ Estado del query: {state}")

        if state == "COMPLETED" or state == "SUCCEEDED":
            print("✅ Datos disponibles")
            # Aquí devolvemos los datos inmediatamente
            return result['result']['records']

        elif state == "FAILED":
            return {"error": "Query failed", "details": result}

        time.sleep(2)

    return {"error": "Timeout", "message": "La consulta no se completó después de varios intentos"}


def disponibilidad(db: Session):
    url = 'https://api.newrelic.com/graphql'
    token = get_by_id(db,'23fc730f-7acd-4727-b157-43152cfa02de')

    query = f"""
    {{
      actor {{
        account(id: 3040357){{
          nrql(query: "SELECT average(numeric(procentaje_disponibilidad_num)) as 'Canales Digitales' from Log_Dispo2024 where nombre like 'SUPERAPP DAVIVIENDA' and hostname = 'SADGBACGS' LIMIT max since 12 month ago FACET Mes"){{
            results
          }}
        }}
      }}
    }}
    """

    headers = {
        'API-Key': token.token,
        'Content-Type': 'application/json'
    }

    body = {
        "query": query,
        "variables": ""
    }

    response = requests.post(url, json=body, headers=headers)
    return response.json()['data']['actor']['account']['nrql']['results']


def number_month(month: str):
    month_list = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                  'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    
    month = month.lower().strip()
    print(month)
    
    if month in month_list:
        return month_list.index(month) + 1
    else:
        raise ValueError(f"Mes inválido: '{month}'")
