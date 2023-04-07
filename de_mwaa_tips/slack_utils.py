def make_slack_fail_notification_v1(task_id, dag_id, ts_logical_time, ts_execution_time, log_url):
    slack_msg = f"""
        :x: Task Failed.
        *Task*: {task_id}
        *Dag*: {dag_id}
        *Logical Date*: {ts_logical_time}
        *Execution Date*: {ts_execution_time}
        <{log_url}|*Logs*>
    """
    return slack_msg

def make_slack_notification_v1(execution_date, dag_id, titulo, msg, taskIniEmptySeq01, taskEndEmptySeq01):
    seconds = 0
    try:
        if taskIniEmptySeq01.start_date is not None and taskEndEmptySeq01.end_date is not None:
            seconds = taskEndEmptySeq01.end_date - taskIniEmptySeq01.start_date
    except:
        seconds = 0

    slack_msg = f"""
    :verifybadge: {titulo}
    *Dag*: {dag_id}
    *Execution Time*: {execution_date}
    *Total Time*: {seconds}
    *Msg*: {msg}
    """
    return slack_msg
