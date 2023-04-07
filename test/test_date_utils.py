import sys
sys.path.insert(0, f'../de_mwaa_tips/')
from de_mwaa_tips import date_utils

def test_get_date_execution_ts_v1():
    str_datetime = date_utils.get_date_execution_ts_v1('2023-04-07 23:59:59', None, 0)
    print(f'str_datetime: {str_datetime}')
    assert str_datetime == '2023-04-07'

def test_get_datetime_execution_ts_v1():
    str_datetime = date_utils.get_datetime_execution_ts_v1('2023-04-07 23:59:59', None, 0)
    str_datetime_iso = date_utils.get_datetime_execution_ts_v1('2023-04-07T23:59:59', None, 0)
    print(f'str_datetime: {str_datetime}')
    assert str_datetime == '2023-04-07 23:59:59' and str_datetime_iso == '2023-04-07 20:59:59'
