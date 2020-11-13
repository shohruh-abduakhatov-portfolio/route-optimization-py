from geo import get_route_matrix
from model import _serialize


class Data:
    def __init__(self):
        pass


    def serialize(self, value):
        _data, _driver, _order = _serialize(_data=value)
        self._data = _data
        self._driver = _driver
        self._order = _order
        self._update_matrix()


    def _update_matrix(self):
        osrm_matrix = get_route_matrix(self._order['latlong'])
        self._data['distance_matrix'] = osrm_matrix['result']['distance'].astype('int').tolist()
        self._data['time_matrix'] = osrm_matrix['result']['time'].astype('int').tolist()
