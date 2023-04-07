from datetime import datetime, timedelta

def datetime_UTC_SaoPaulo(str_datetime_logical, str_datetime_params, int_days=0):
    if str_datetime_params is not None:
        str_datetime = str(str_datetime_params)
    else:
        str_datetime = str(str_datetime_logical)

    print(f'''get_date_execution_ts - str_datetime_logical: {str_datetime_logical} - str_datetime_params: {str_datetime_params} - int_days: {int_days}''')


    if str_datetime.find('+') > 0:
        str_datetime = str_datetime[0:str_datetime.find('+')]

    if str_datetime.find('.') > 0:
        str_datetime = str_datetime[0:str_datetime.find('.')]

    if str_datetime.find('T') > -1:
        datetime_logical =  datetime.strptime(str_datetime, '%Y-%m-%dT%H:%M:%S')
        # Server running always UTC
        t_hours = timedelta(hours=3)
        datetime_logical = datetime_logical - t_hours
    elif (len(str_datetime) > 10 and str_datetime.find(' ') > 0):
        datetime_logical =  datetime.strptime(str_datetime, '%Y-%m-%d %H:%M:%S')
    else:
        datetime_logical =  datetime.strptime(f'{str_datetime} 00:00:00', '%Y-%m-%d %H:%M:%S')

    t_days = timedelta(days=int_days)
    sub_datetime_logical = datetime_logical - t_days 
    
    return sub_datetime_logical

def get_date_execution_ts_v1(str_datetime_logical, str_datetime_params, int_days=0):
    sub_datetime_logical = datetime_UTC_SaoPaulo(str_datetime_logical, str_datetime_params, int_days)
    str_datetime_return = sub_datetime_logical.date().strftime("%Y-%m-%d")
    return str_datetime_return

def get_datetime_execution_ts_v1(str_datetime_logical, str_datetime_params, int_days=0):
    sub_datetime_logical = datetime_UTC_SaoPaulo(str_datetime_logical, str_datetime_params, int_days) 
    return sub_datetime_logical.strftime("%Y-%m-%d %H:%M:%S")

def get_date_now_v1():
    datetime_now = datetime.now()
    t_hours = timedelta(hours=3)
    datetime_logical = datetime_now - t_hours
    print(f"datetime_logical: {datetime_logical}")
    return datetime_logical.date().strftime("%Y-%m-%d")

def get_datetime_now_v1():
    datetime_now = datetime.now()
    t_hours = timedelta(hours=3)
    datetime_logical = datetime_now - t_hours
    print(f"datetime_logical: {datetime_logical}")
    return datetime_logical.strftime("%Y-%m-%d %H:%M:%S")
