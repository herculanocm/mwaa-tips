import logging
from typing import Any
from boto3 import client
from botocore.exceptions import ClientError, ParamValidationError
from de_mwaa_tips.logger_utils import get_logger
import urllib3
import json
from base64 import b64decode
from datetime import datetime


def get_mwaa_cli_response(client_mwaa: client, mwaa_env_name: str, logger: logging.Logger = None) -> Any:
    logger = get_logger(logger)
    try: 
        mwaa_cli_response = client_mwaa.create_cli_token( Name=mwaa_env_name )
        return mwaa_cli_response
    except ClientError as e:
        # Handle ClientError, log or raise a specific exception
        logger.error(f"Error creating CLI token: {e}")
        # Handle or raise an appropriate exception based on your application logic
    except ParamValidationError as e:
        # Handle ParamValidationError, log or raise a specific exception
        logger.error(f"Invalid parameters: {e}")
        # Handle or raise an appropriate exception based on your application logic
    except Exception as e:
        # Handle any other unexpected exceptions
        logger.error(f"Unexpected error: {e}")
        # Log or raise an appropriate exception based on your application logic
    return None

def get_mwaa_cli_token_from_response(mwaa_cli_response: Any, logger: logging.Logger = None) -> str:
    logger = get_logger(logger)
    if (
        mwaa_cli_response is None or 
        isinstance(mwaa_cli_response, dict) == False or
        'CliToken' not in mwaa_cli_response
        ):
        logger.warn("CliToken don't exists in response")
        return None
    
    return mwaa_cli_response['CliToken']

def get_mwaa_web_server_hostname_from_response(mwaa_cli_response: Any, logger: logging.Logger = None) -> str:
    logger = get_logger(logger)
    if (
        mwaa_cli_response is None or 
        isinstance(mwaa_cli_response, dict) == False or
        'WebServerHostname' not in mwaa_cli_response
        ):
        logger.warn("WebServerHostname don't exists in response")
        return None
    
    return mwaa_cli_response['WebServerHostname']

def mwaa_trigger_dag_by_client(client_mwaa: client, mwaa_env_name: str, dag_name: str, exec_date: datetime = None, dag_conf: dict = None, run_id: str = None, logger: logging.Logger = None)-> urllib3.response.HTTPResponse:
    logger = get_logger(logger)

    mwaa_cli_response = get_mwaa_cli_response(client_mwaa=client_mwaa, mwaa_env_name=mwaa_env_name, logger=logger)
    mwaa_webserver_hostname = get_mwaa_web_server_hostname_from_response(mwaa_cli_response, logger=logger)
    mwaa_jwt_token = get_mwaa_cli_token_from_response(mwaa_cli_response, logger=logger)

    return mwaa_trigger_dag(mwaa_webserver_hostname, dag_name, mwaa_jwt_token, exec_date, dag_conf, run_id, logger)
    
def mwaa_trigger_dag(mwaa_webserver_hostname: str, dag_name: str, mwaa_jwt_token: str, exec_date: datetime = None, dag_conf: dict = None, run_id: str = None, logger: logging.Logger = None) -> urllib3.response.HTTPResponse:
    logger = get_logger(logger)

    logger.info('Enconding dag_conf')
    raw_dag_conf = '{}'
    if dag_conf is not None and isinstance(dag_conf, dict):

        try:
            raw_dag_conf = json.dumps(dag_conf, ensure_ascii=False)
        except Exception as e:
            # Handle any other unexpected exceptions
            logger.error(f"Unexpected error while encoding dag_conf: {e}")

        logger.info('dag_conf encoded')

    logger.info('Getting exec_date from datetime')
    raw_exec_date = ''
    if exec_date is not None and isinstance(exec_date, datetime):
        raw_exec_date = f'''--exec-date "{exec_date.strftime("%Y-%m-%d %H:%M:%S")}"'''
        logger.info('exec_date getted')

    logger.info('Getting run_id')
    raw_run_id = ''
    if run_id is not None and isinstance(run_id, str):
        raw_exec_date = f"""--run-id {run_id}"""
        logger.info('run_id getted')


    raw_data = f"""dags trigger {dag_name} --conf '{raw_dag_conf}' {raw_exec_date} {raw_run_id} """
    logger.info(f'raw_data: {raw_data}')

    headers_authentication = {
        'Content-Type': 'text/plain',
        'Authorization': ('Bearer %s' % mwaa_jwt_token)
    }

    mwaa_webserver_hostname = f"https://{mwaa_webserver_hostname}/aws_mwaa/cli"

    logger.info(f"""Posting on: {mwaa_webserver_hostname} - Dag name: {dag_name}""")

    try:
        http = urllib3.PoolManager()
        resp = http.request('POST', mwaa_webserver_hostname,
                            body=raw_data, headers=headers_authentication)
        return resp
    except urllib3.exceptions.MaxRetryError as e:
        logger.error(f"Max retries exceeded: {e}")
    except urllib3.exceptions.TimeoutError as e:
        logger.error(f"Request timed out: {e}")
    except urllib3.exceptions.HTTPError as e:
        logger.error(f"HTTP error: {e}")
    except urllib3.exceptions.RequestError as e:
        logger.error(f"Request error: {e}")
    except urllib3.exceptions.ConnectionError as e:
        logger.error(f"Connection error: {e}")
    except urllib3.exceptions.PoolError as e:
        logger.error(f"Pool error: {e}")
    except urllib3.exceptions.ProxyError as e:
        logger.error(f"Proxy error: {e}")
    except urllib3.exceptions.SSLError as e:
        logger.error(f"SSL/TLS error: {e}")
    except urllib3.exceptions.DecodeError as e:
        logger.error(f"Decode error: {e}")
    except urllib3.exceptions.ProtocolError as e:
        logger.error(f"Protocol error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    return None


def mwaa_b64_decode_std(raw_decoded_json: str, logger: logging.Logger = None) -> dict:
    logger = get_logger(logger)
    try:
        logger.info('Converting raw_json to dict')
        dict_resp = json.loads(raw_decoded_json)
        logger.info('Raw_json converted to dict')
    except Exception as e:
            # Handle any other unexpected exceptions
            logger.error(f"Error converting raw_json to dict: {e}")
            logger.error(f"Value: {raw_decoded_json}")
            return None

    for key, value in dict_resp.items():
        dict_resp[key] = b64decode(value)

    return dict_resp


