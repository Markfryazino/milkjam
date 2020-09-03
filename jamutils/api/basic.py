import requests
from .. import API_URL


def start_run(params):
    """
    Method that starts another run.
    :param params: can contain: name, start_time (default is current), comment, start_balance (default is 200)
    :return: status code and the dump of the Run object or a mistake message
    """

    response = requests.get(url=API_URL + 'start-run', params=params)
    if response.status_code == 200:
        return response.status_code, eval(response.content.decode('ascii'))
    else:
        return response.status_code, response.content.decode('ascii')


def get_snapshot(run_id, timestamp):
    """
    Method that gets the snapshot of a moment during the run.
    :param run_id: ID of the run
    :param timestamp: datetime object
    :return: status code and the dump of the Snapshot object or a mistake message
    """

    params = {'run_id': run_id, 'timestamp': timestamp}
    response = requests.get(url=API_URL + 'get-snapshot', params=params)
    if response.status_code == 200:
        return response.status_code, eval(response.content.decode('ascii'))
    else:
        return response.status_code, response.content.decode('ascii')


def make_action(run_id, timestamp, query):
    """
    Tries to sell or buy coins.
    :param run_id: ID of the run
    :param timestamp: datetime object
    :param query: dict of format {pair: volume}. If volume is positive, it will be bought, otherwise sold.
    :return: status code and the dump of the Action object or a mistake message
    """

    params = {'run_id': run_id, 'timestamp': timestamp, 'query': str(query)}
    response = requests.get(url=API_URL + 'make_action', params=params)
    if response.status_code == 200:
        return response.status_code, eval(response.content.decode('ascii'))
    else:
        return response.status_code, response.content.decode('ascii')


def end_run(run_id, timestamp):
    """
    Finishes the run and sells all coins.
    :param run_id: ID of the run
    :param timestamp: datetime object
    :return: status code and the dump of the Run object or a mistake message
    """

    params = {'run_id': run_id, 'timestamp': timestamp}
    response = requests.get(url=API_URL + 'end-run', params=params)
    if response.status_code == 200:
        return response.status_code, eval(response.content.decode('ascii'))
    else:
        return response.status_code, response.content.decode('ascii')
