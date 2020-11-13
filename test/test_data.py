import asyncio

from data import Data
from pdp import main


main_loop = asyncio.get_event_loop()

_input = {'drivers': {'1': {'car_speed': 1, 'car_type': 2}, '2': {'car_speed': 100, 'car_type': 2}}, 'orders': {
    '4': {'pick_time_window': 1579016931, 'pick_time_window_end': 1579019931, 'drop_time_window': 1579042133,
          'drop_time_window_end': 1579092133, 'pick_lat': 41.123456, 'pick_long': 69.235467, 'drop_lat': 41.123456,
          'drop_long': 69.123456, 'capacity': 1, 'weight': 2.0}}}


async def _main():
    _data = Data()
    _data.serialize(value=_input)
    response = {}
    try:
        response = await main(_data)
    except Exception as e:
        print(e)
    return response

main_loop.create_task(_main())
main_loop.run_forever()