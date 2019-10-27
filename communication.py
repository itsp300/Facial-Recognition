import json
import queue
import time
from typing import Dict, AnyStr, Callable

import jwt
import websocket

websocket_message_types = {}  # type: Dict[AnyStr, Callable]
websocket_access_token = ""  # type: AnyStr
request_queue = queue.Queue()
debug = False
communication_version = "1"


def err_disp_hand(err):
    pass


err_display_handler = err_disp_hand


def debug_log(message):
    if debug:
        print("[Communication]" + str(message))


def log_err(err):
    print("[Communication][ERR]" + str(err))

# either have config.json, or set manually here, delete file part if dont want to do config
with open("config.json", encoding='utf-8') as file:
    config_data = json.loads(file.read())
    jwt_signature = str(config_data['jwt_signature']).strip()
    api_path = str(config_data['api_path']).strip().strip()
    client_id = str(config_data['client_id']).strip()
    client_secret = str(config_data['client_secret']).strip()
    audience = str(config_data['audience']).strip()
    domain = str(config_data['domain']).strip()
    if 'use_ssl' in config_data:
        use_ssl = bool(config_data['use_ssl'])
    else:
        use_ssl = True
    debug_log("Configuration File Read Successfully")


def register_message_type(type_name: str, method: callable):
    debug_log("Registered message type '" + type_name + "'")
    global websocket_message_types
    websocket_message_types[type_name] = method


def start_websocket():
    global websocket_access_token
    websocket_access_token = new_access_token()
    websocket.enableTrace(debug)
    if use_ssl:
        protocol = "wss://"
    else:
        protocol = "ws://"
    ws = websocket.WebSocketApp(protocol + api_path + "/",
                                on_message=websocket_message,
                                on_error=websocket_error,
                                on_close=websocket_close)
    ws.on_open = websocket_open
    return ws


def websocket_open(ws):
    print("Web Socket Open")
    debug_log("Websocket Open")
    auth_message = {
        'access_token': ensure_valid(websocket_access_token),
        'type': 'auth_face'
    }
    request_send_jwt(auth_message)


def websocket_error(ws, error):
    log_err("Error: " + str(error))
    err_display_handler(error)


def websocket_close(ws):
    debug_log("Websocket Closed")


def websocket_message(ws, message):
    debug_log("Websocket Message Inbound: " + str(message))
    jwt_payload = decode_jwt(message)
    if jwt_payload is None:
        return
    for t in websocket_message_types:
        if jwt_payload['type'] == t:
            if callable(websocket_message_types[t]):
                websocket_message_types[t](jwt_payload)
                debug_log("Inbound Websocket Message Matched with " + t)
                return
    debug_log("Inbound Websocket Message -- No Matches found")


def ensure_valid(access_token):
    if access_token is not str:
        return new_access_token()
    if access_token != "" and access_token is not None:
        eat = decode_jwt(access_token)
        if eat is not None:
            eat = eat['eat']
        else:
            return new_access_token()
        if time.time() < eat:
            return access_token
    return new_access_token()


def new_access_token():
    import requests
    payload = {"client_id": client_id,
               "client_secret": client_secret,
               "audience": audience,
               "grant_type": "client_credentials"}
    result = requests.post("https://" + domain + "/connect/token", data=payload).json()
    if 'error' in result:
        raise Exception("Access Token: " + str(result['error']))
    else:
        access_token = result['access_token']
    debug_log("Access Token: " + access_token)
    time.sleep(1)  # Sleep for 1s since not doing this will cause jwt error, because iat too recent
    return access_token


def decode_jwt(jwt_message):
    from jwt import InvalidSignatureError
    global jwt_signature
    try:
        return jwt.decode(jwt_message, key=jwt_signature)
    except InvalidSignatureError as error:
        debug_log("Invalid Key Provided!")
        debug_log("Error: " + str(error))
    return None


def encode_jwt(jwt_message):
    global jwt_signature
    return jwt.encode(jwt_message, key=jwt_signature)


def request_send_jwt(data: Dict):
    if "version" not in data:
        data['version'] = communication_version
    payload = json.loads(json.dumps(data))
    jwt_request = encode_jwt(payload)
    request_queue.put(jwt_request)
