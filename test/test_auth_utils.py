import sys
sys.path.insert(0, f'../mwaa-tips/')
print(sys.path)
from de_mwaa_tips import auth_utils
import boto3
from de_mwaa_tips import logger_utils
from datetime import datetime

def test_auth_utils():
    aws_access_key_id=''
    aws_secret_access_key=''
    aws_session_token=''
    mwaa_env_name = 'airflow-analytics'

    client = boto3.client('mwaa',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token,
                        region_name='us-east-1'
                        )

    logger = logger_utils.get_logger()
    dict_ret = auth_utils.mwaa_trigger_dag_by_client(client_mwaa=client, mwaa_env_name=mwaa_env_name, dag_name='datalake_run_test_dummy', dag_conf={'chave': 'teste'}, exec_date=datetime(2022, 8, 11, 12 , 57, 59), run_id="manual_1234565_id", logger = logger)
    decoded = auth_utils.mwaa_b64_decode_std(dict_ret.data.decode("utf-8"), logger = logger)

    print(decoded)
    assert 1 == 1

test_auth_utils()