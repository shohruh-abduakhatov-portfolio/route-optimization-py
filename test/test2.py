import asyncio

from data import Data
from pdp import main


main_loop = asyncio.get_event_loop()

_input = {'drivers': {'1': {'car_speed': 70, 'car_type': 1}, '2': {'car_speed': 60, 'car_type': 1}}, 'orders': {'1': {'pick_time_window': 1578958770.0, 'drop_time_window': 1579131572.0, 'pick_time_window_end': 1579134478.0, 'drop_time_window_end': 1579134480.0, 'pick_lat': 41.311701, 'pick_long': 69.273097, 'drop_lat': 41.311917, 'drop_long': 69.286225, 'capacity': 2, 'weight': 1.0}, '3': {'pick_time_window': 1579021265.0, 'drop_time_window': 1579280466.0, 'pick_time_window_end': 1579134447.0, 'drop_time_window_end': 1579307251.0, 'pick_lat': 41.257785, 'pick_long': 69.336828, 'drop_lat': 41.28539, 'drop_long': 69.215334, 'capacity': 3, 'weight': 4.0}, '4': {'pick_time_window': 1580842578.0, 'drop_time_window': 1581015387.0, 'pick_time_window_end': 1580928980.0, 'drop_time_window_end': 1581101798.0, 'pick_lat': 41.304158, 'pick_long': 69.306515, 'drop_lat': 41.272323, 'drop_long': 69.165712, 'capacity': 1, 'weight': 2.0}, '5': {'pick_time_window': 1581010391.0, 'drop_time_window': 1581096795.0, 'pick_time_window_end': 1581013993.0, 'drop_time_window_end': 1581183213.0, 'pick_lat': 41.29947205772315, 'pick_long': 69.22803220467634, 'drop_lat': 41.309341035308066, 'drop_long': 69.23837184906006, 'capacity': 1, 'weight': 1.0}, '6': {'pick_time_window': 1580999686.0, 'drop_time_window': 1581096902.0, 'pick_time_window_end': 1581010499.0, 'drop_time_window_end': 1581183305.0, 'pick_lat': 41.30085840684354, 'pick_long': 69.2291050882823, 'drop_lat': 41.30087237768648, 'drop_long': 69.23047837929792, 'capacity': 1, 'weight': 1.0}, '7': {'pick_time_window': 1581010522.0, 'drop_time_window': 1581096926.0, 'pick_time_window_end': 1581096923.0, 'drop_time_window_end': 1581197728.0, 'pick_lat': 41.299149646727344, 'pick_long': 69.22335443215437, 'drop_lat': 41.30158166103747, 'drop_long': 69.22515687661237, 'capacity': 1, 'weight': 1.0}, '8': {'pick_time_window': 1581010667.0, 'drop_time_window': 1581183482.0, 'pick_time_window_end': 1581097069.0, 'drop_time_window_end': 1581269886.0, 'pick_lat': 41.29821464582645, 'pick_long': 69.2508631678111, 'drop_lat': 41.29532680557521, 'drop_long': 69.22335443215437, 'capacity': 1, 'weight': 1.0}, '2': {'pick_time_window': 1579131843.0, 'drop_time_window': 1579304653.0, 'pick_time_window_end': 1579134466.0, 'drop_time_window_end': 1579320869.0, 'pick_lat': 41.331208, 'pick_long': 69.25274, 'drop_lat': 41.329395, 'drop_long': 69.254199, 'capacity': 4, 'weight': 2.0}}}


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