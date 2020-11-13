
"""
'drivers': {
        'driver_id_1': {
            'car_type': ['a','b'], 
            'car_speed': 0.5 # (0,2]
        }, 
        'driver_id_2':{
        ...
        }
    }
    
 'orders':{
        'order_id_1': {
            'pick_time_window': timestamp,
            'drop_time_window': timestamp,
            'pick_lat': lattitude: flaot,
            'pick_long': longitude: float,
            'drop_lat': --
            'drop_long': --
            'capacity': 1 # volume of the order
            'weight': # weight of the order
            'car_type': ['a'], # should match 'car_type'. Can be empty
        }, 
        'order_id_2': {
            ...
        }
    }
"""

# todo convert to unix

import datetime


dt_fmt = '%Y-%m-%d %H:%M:%S.%f'


def to_unix(dt):
    _dt = datetime.datetime.strptime(dt, dt_fmt)
    return int(_dt.timestamp())


def refresh_data():
    data = {
        'distance_matrix': [],
        'time_matrix': [],
        'time_windows': [],
        'num_vehicles': [],
        'depot': [],
        'vehicle_capacities': [],
        'vehicle_weights': [],
        'allow_return': True
    }

    data["start_end"] = [data['depot']]

    driver = {
        'id': [],
        'type': {},
        'speed': []
    }

    order = {
        'id': [],
        'order_id': [],
        'time_window': [],
        'latlong': [],
        'capacity': [],
        'weight': [],
        'car_type': [],
        'type': [],
        'pickups_deliveries': [],
    }

    return data, driver, order


def _serialize(_data):
    data, driver, order = refresh_data()
    for driver_index, (driver_id, value) in enumerate(_data['drivers'].items()):
        driver['id'].append(str(driver_id))
        if not isinstance(value['car_type'], (list, tuple)):
            value['car_type'] = [value['car_type']]
        driver['speed'].append(value['car_speed'])
        for _type in value['car_type']:
            try:
                driver['type'][str(_type)].append(driver_index)
            except:
                driver['type'][str(_type)] = [driver_index]
    data['num_vehicles'] = len(driver['id'])
    order_index = 1
    # order
    order['id'] += ['Depot']
    order['order_id'] += ['Depot']
    order['time_window'] += [None]
    order['latlong'] += [[69.283962, 41.316778]]
    order['capacity'] += [0]
    order['type'] += ['pick']
    order['weight'] += [0]
    order['car_type'] += [None]
    for order_id, value in _data['orders'].items():
        order['id'] += [str(order_id)+"_pick", str(order_id)+"_drop"]
        order['order_id'] += [str(order_id), str(order_id)]
        ptw = [int(value['pick_time_window']), int(value['pick_time_window_end'])]
        dtw = [int(value['drop_time_window']), int(value['drop_time_window_end'])]
        order['time_window'] += [ptw, dtw]
        order['latlong'] += [
            [value['pick_long'], value['pick_lat']],
            [value['drop_long'], value['drop_lat']],
        ]
        order['type'] += ['pick', 'drop']
        order['capacity'] += [value.get('capacity', 1)] * 2
        order['weight'] += [int(value.get('weight', 1))] * 2
        order['car_type'] += [value.get('car_type'), None]
        order['pickups_deliveries'] += [[order_index, order_index + 1]]
        order_index += 2
    # depot
    _flat_time_windows = []
    for time_window in order['time_window'][1:]:
        _flat_time_windows.append(time_window[0])
        _flat_time_windows.append(time_window[1])
    data['min_horizon'] = min(_flat_time_windows)
    data['max_horizon'] = max(_flat_time_windows)
    data['depot'] = 0
    data['vehicle_capacities'] = [100] * len(driver['id'])
    data['vehicle_weights'] = [1000] * len(driver['id'])
    data['horizon'] = data['max_horizon'] - data['min_horizon']
    return data, driver, order

def deserialize():
    pass
