from typing import Optional, Tuple, Union, Dict, Any
import requests
import time
from sqlalchemy.orm import Session
from repositories.token_repository import get_by_id
from datetime import date, datetime, timedelta

URLV2 = 'https://esd62814.live.dynatrace.com/api/v2/metrics/query'
URLV1 = 'https://esd62814.live.dynatrace.com/api/v1/userSessionQueryLanguage/table'
URLNEWRELIC = 'https://api.newrelic.com/graphql'
URLOAUTH = 'https://esd62814.apps.dynatrace.com/platform/storage/query/v1/query:poll'
URLTOKEN = 'https://sso.dynatrace.com/sso/oauth2/token'
URLREQUESTTOKEN = 'https://esd62814.apps.dynatrace.com/platform/storage/query/v1/query:execute'

def dates(start_date: Optional[date] = None, end_date: Optional[date] = None) -> Tuple[int, int]:
    if not start_date:
        timestamp_start = int((datetime.now() - timedelta(hours=2)).timestamp() * 1000)
    else:
        timestamp_start = int(datetime.combine(start_date, datetime.min.time()).timestamp() * 1000)

    if not end_date:
        timestamp_end = int(datetime.now().timestamp() * 1000)
    else:
        timestamp_end = int(datetime.combine(end_date, datetime.min.time()).timestamp() * 1000)

    print('Tiempos:', timestamp_start, timestamp_end)
    return timestamp_start, timestamp_end

def create_token(db: Session):
    token = get_by_id(db, 'c052574a-9e1f-46cf-9d6e-6f87d2138c23')
    body = {
        'client_id': 'dt0s02.5X2A7NYQ',
        'grant_type': 'client_credentials',
        'client_secret': f'{token.token}',
        'resource': 'urn:dtaccount:5d8555d6-ac2e-4fca-82dd-d32e718916c4'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'AWSALB=7od9vDqM6B53dgMX3g5iWINGXnM2/uBdda5Hd8c9YPa0du/ox9ng5mDl0+D+x7siAW1gCfAH55oUGWIw5ePaMOhObRg4ei9s5DgfrTV+SmbLN+wkBkPu/yeP82JL; AWSALBCORS=7od9vDqM6B53dgMX3g5iWINGXnM2/uBdda5Hd8c9YPa0du/ox9ng5mDl0+D+x7siAW1gCfAH55oUGWIw5ePaMOhObRg4ei9s5DgfrTV+SmbLN+wkBkPu/yeP82JL'
    }
    response = requests.post(url=URLTOKEN, data=body, headers=headers)
    return response.json()['access_token']

def query(db: Session):
    token = create_token(db)
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
    response = requests.post(url=URLREQUESTTOKEN, json=body, headers=headers)
    return response.json()['requestToken']

def data(db: Session):
    token = create_token(db)
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
        response = requests.get(url=URLOAUTH, params=body, headers=headers)

        try:
            result = response.json()
        except requests.exceptions.JSONDecodeError:
            return {"error": "Invalid JSON", "body": response.text}

        state = result.get("state")
        print(f"⏳ Estado del query: {state}")

        if state == "COMPLETED" or state == "SUCCEEDED":
            print("✅ Datos disponibles")
            return result['result']['records']

        elif state == "FAILED":
            return {"error": "Query failed", "details": result}

        time.sleep(2)

    return {"error": "Timeout", "message": "La consulta no se completó después de varios intentos"}

def disponibilidad(db: Session):
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

    response = requests.post(URLNEWRELIC, json=body, headers=headers)
    return response.json()['data']['actor']['account']['nrql']['results']

def apdex_metrics(db: Session, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    token = get_by_id(db, '60e4daec-19f7-4cc7-a5fa-74c23cad2bf7')
    timestamp_start, timestamp_end = dates(start_date, end_date)
    
    headers = {
        'accept': 'application/json',
        'Authorization': f'Api-Token {token.token}'
    }
    web_params = {
        'metricSelector': '(builtin:apps.web.apdex.userType:filter(and(or(in("dt.entity.application",entitySelector("type(application),entityName.equals(~Superapp Web~)"))))):splitBy():sort(value(auto,descending)):limit(20)):limit(100):names',
        'from': timestamp_start,
        'to': timestamp_end,
        'resolution': 'Inf',
        'mzSelector': 'mzId(6734853283526883009)'
    }
    mobile_params = {
        'metricSelector': '(builtin:apps.other.apdex.osAndVersion:filter(and(or(in("dt.entity.device_application",entitySelector("type(mobile_application),entityName.equals(~"SuperApp~")"))))):splitBy():sort(value(auto,descending)):limit(100)):limit(100):names',
        'from': timestamp_start,
        'to': timestamp_end,
        'resolution': 'Inf',
        'mzSelector': 'mzId(6734853283526883009)'
    }
    result = {}
    web_response = requests.get(url=URLV2, headers=headers, params=web_params)
    if web_response.status_code == 200:
        result['web'] = web_response.json()['result'][0]['data'][0]['values'][0]
    else:
        result['web'] = {"error": web_response.status_code, "message": web_response.text}
    mobile_response = requests.get(url=URLV2, headers=headers, params=mobile_params)
    if mobile_response.status_code == 200:
        result['mobile'] = mobile_response.json()['result'][0]['data'][0]['values'][0]
    else:
        result['mobile'] = {"error": mobile_response.status_code, "message": mobile_response.text}
    
    return result

def session_metrics(db: Session, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    token = get_by_id(db, '60e4daec-19f7-4cc7-a5fa-74c23cad2bf7')
    timestamp_start, timestamp_end = dates(start_date, end_date)
    
    headers_v1 = {
        'Authorization': f'Api-Token {token.token}'
    }
    headers_v2 = {
        'accept': 'application/json',
        'Authorization': f'Api-Token {token.token}'
    }
    result = {}
    unique_params = {
        'query': "SELECT COUNT(DISTINCT(internalUserId)) FROM usersession WHERE ((useraction.application='SuperApp' OR userevent.application='SuperApp' OR usererror.application='SuperApp')) AND userId IS NOT NULL",
        'startTimestamp': timestamp_start,
        'endTimestamp': timestamp_end,
    }
    
    unique_response = requests.get(url=URLV1, headers=headers_v1, params=unique_params)
    if unique_response.status_code == 200:
        unique_sessions = unique_response.json()['values'][0][0]
        result['unique_sessions'] = unique_sessions*2
    else:
        result['unique_sessions'] = {"error": unique_response.status_code, "message": unique_response.text}
    
    total_params = {
        'metricSelector': '(builtin:apps.mobile.sessionCount:filter(and(or(in("dt.entity.mobile_application",entitySelector("type(mobile_application),entityName.equals(~"SuperApp~")"))))):splitBy():sort(value(auto,descending)):limit(20)):limit(100):names',
        'from': timestamp_start,
        'to': timestamp_end,
        'resolution': 'Inf',
        'mzSelector': 'mzId(6734853283526883009)'
    }
    
    total_response = requests.get(url=URLV2, headers=headers_v2, params=total_params)
    if total_response.status_code == 200:
        total_sessions = total_response.json()['result'][0]['data'][0]['values'][0]
        result['total_sessions'] = total_sessions*2
    else:
        result['total_sessions'] = {"error": total_response.status_code, "message": total_response.text}
    

    if (isinstance(result.get('unique_sessions'), (int, float)) and 
        isinstance(result.get('total_sessions'), (int, float)) and 
        result['unique_sessions'] > 0):
        
        avg_sessions = result['total_sessions'] / result['unique_sessions']
        result['average_sessions_per_user'] = round(avg_sessions, 1)
    else:
        result['average_sessions_per_user'] = {"error": "No se pudieron calcular las sesiones promedio"}
    
    return result

def login_time_by_platform(db: Session, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    token = get_by_id(db, '60e4daec-19f7-4cc7-a5fa-74c23cad2bf7')
    timestamp_start, timestamp_end = dates(start_date, end_date)
    headers = {
        'accept': 'application/json',
        'Authorization': f'Api-Token {token.token}'
    }
    
    ios_params = {
        "metricSelector": '(builtin:apps.other.keyUserActions.duration.os:filter(and(or(in("dt.entity.device_application_method",entitySelector("type(device_application_method),fromRelationship.isDeviceApplicationMethodOf(type(MOBILE_APPLICATION),entityName.equals(~"SuperApp~"))"))),or(in("dt.entity.os",entitySelector("type(os),entityName.equals(~"iOS~")"))),or(in("dt.entity.device_application_method",entitySelector("type(device_application_method),entityName.equals(~"HOM~")")),in("dt.entity.device_application_method",entitySelector("type(device_application_method),entityName.equals(~"Loading MainActivity~")")),in("dt.entity.device_application_method",entitySelector("type(device_application_method),entityName.equals(~"LOG~")")),in("dt.entity.device_application_method",entitySelector("type(device_application_method),entityName.equals(~"Loading Davivienda~")")),in("dt.entity.device_application_method",entitySelector("type(device_application_method),entityName.equals(~"Touch on Iniciar sesión~")"))))):splitBy("dt.entity.device_application_method","dt.entity.os"):avg:sort(value(avg,descending)):limit(20)):names',
        'from': timestamp_start,
        'to': timestamp_end,
        'resolution': 'Inf',
        'mzSelector': 'mzId(6734853283526883009)'
    }
    android_params = {
        "metricSelector": '(builtin:apps.other.keyUserActions.duration.os:filter(and(or(in("dt.entity.os",entitySelector("type(os),entityName.equals(~"Android~")"))),or(in("dt.entity.device_application_method",entitySelector("type(device_application_method),fromRelationship.isDeviceApplicationMethodOf(type(MOBILE_APPLICATION),entityName.equals(~"SuperApp~"))"))),or(in("dt.entity.device_application_method",entitySelector("type(device_application_method),entityName.equals(~"HOM~")")),in("dt.entity.device_application_method",entitySelector("type(device_application_method),entityName.equals(~"Loading MainActivity~")")),in("dt.entity.device_application_method",entitySelector("type(device_application_method),entityName.equals(~"LOG~")")),in("dt.entity.device_application_method",entitySelector("type(device_application_method),entityName.equals(~"Loading Davivienda~")")),in("dt.entity.device_application_method",entitySelector("type(device_application_method),entityName.equals(~"Touch on Iniciar sesión~")"))))):splitBy("dt.entity.device_application_method","dt.entity.os"):avg:sort(value(avg,descending)):limit(20)):names',
        'from': timestamp_start,
        'to': timestamp_end,
        'resolution': 'Inf',
        'mzSelector': 'mzId(6734853283526883009)'
    }
    
    result = {}
    ios_response = requests.get(url=URLV2, headers=headers, params=ios_params)

    if ios_response.status_code == 200:
        ios_data = ios_response.json()['result'][0]['data']
        total_ios = sum(entry['values'][0] for entry in ios_data)
        result['total_ios'] = round(total_ios/1000000, 2)
    else:
        result['ios'] = {"error": ios_response.status_code, "message": ios_response.text}
        result['total_ios'] = None

    android_response = requests.get(url=URLV2, headers=headers, params=android_params)
    if android_response.status_code == 200:
        android_data = android_response.json()['result'][0]['data']
        total_android = sum(entry['values'][0] for entry in android_data)
        result['total_android'] = round(total_android/1000000, 2)
    else:
        result['android'] = {"error": android_response.status_code, "message": android_response.text}
        result['total_android'] = None
    
    return result

def app_version(db: Session):
    token = get_by_id(db, '60e4daec-19f7-4cc7-a5fa-74c23cad2bf7')
    params = {
        'metricSelector': '(builtin:apps.other.uaCount.osAndVersion:splitBy("App Version"):value:sort(value(sum,descending)):limit(5)):limit(100):names',
        'resolution': 'Inf',
        'mzSelector': 'mzId(6734853283526883009)'
    }
    headers = {
        'accept': 'application/json',
        'Authorization': f'Api-Token {token.token}'
    }
    response = requests.get(url=URLV2, headers=headers, params=params)
    result = {}
    if response.status_code == 200:
        versions = response.json()['result'][0]['data']
        version_dict = {}
        for entry in versions:
            version_name = entry['dimensions'][0]
            user_count = entry['values'][0]
            version_dict[version_name] = user_count
        result   = version_dict
        return result
    else:
        return {"error": response.status_code, "message": response.text}