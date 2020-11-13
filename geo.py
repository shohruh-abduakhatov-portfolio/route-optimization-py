from urllib import request
from urllib.error import HTTPError

import numpy as np
import requests
import json

from config import config as conf
from utils import Unit


def get_route_matrix(nodes_list, convert_to=Unit.km):
    """
    :param nodes_list: [long,lat]
    :return:
    # req = 'http://34.254.124.76/table/v1/driving/41.300108,69.236803;41.292050,69.222986;41.283795,69.236143?annotations=distance' """
    coords_request = str(nodes_list).replace(" ", "").replace("],[", ";").replace("),(", ";").strip('[()]').strip('[[]]')
    headers = {}
    headers['Content-Type'] = 'application/json'
    req = 'http://%s/table/v1/driving/%s?annotations=distance' % (conf.osrm_host, coords_request)
    try:
        output = request.urlopen(req).read()
        output = output.decode("utf-8")
    except:
        req += '&continue_straight=false'
        try:
            output = request.urlopen(req).read()
            output = output.decode("utf-8")
        except:
            output = requests.post(req)
    matrix = json.loads(output)
    try:
        res_dict = {}
        durations_matrix = (np.array(matrix['distances']) * 2 / 1000).astype('int')
        if convert_to == Unit.km:
            res_dict['distance'] = (np.array(matrix['distances']) / 1000).round(2)
            res_dict['time'] = np.ceil(durations_matrix).astype('int')
        else:
            res_dict['distance'] = matrix['distances']
            res_dict['time'] = durations_matrix
    except TypeError as type_err:
        print(type_err, "\n**** Error -> ConnectionResetError: [Errno 104] Connection reset by peer")
        raise HTTPError('**** Error -> ConnectionResetError: [Errno 104] Connection reset by peer')
    except:
        return None
    result = {}
    result['coordinates'] = nodes_list
    result['result'] = res_dict
    return result
