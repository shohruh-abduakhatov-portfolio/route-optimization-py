"""Vehicles Routing Problem (VRP)."""

from __future__ import print_function

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

from helper import *


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = [
        [
            0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354,
            468, 776, 662
        ],
        [
            548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674,
            1016, 868, 1210
        ],
        [
            776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164,
            1130, 788, 1552, 754
        ],
        [
            696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822,
            1164, 560, 1358
        ],
        [
            582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708,
            1050, 674, 1244
        ],
        [
            274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628,
            514, 1050, 708
        ],
        [
            502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856,
            514, 1278, 480
        ],
        [
            194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320,
            662, 742, 856
        ],
        [
            308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662,
            320, 1084, 514
        ],
        [
            194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388,
            274, 810, 468
        ],
        [
            536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764,
            730, 388, 1152, 354
        ],
        [
            502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114,
            308, 650, 274, 844
        ],
        [
            388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194,
            536, 388, 730
        ],
        [
            354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0,
            342, 422, 536
        ],
        [
            468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536,
            342, 0, 764, 194
        ],
        [
            776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274,
            388, 422, 764, 0, 798
        ],
        [
            662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730,
            536, 194, 798, 0
        ],
    ]
    data['time_matrix'] = [
        [0, 6, 9, 8, 7, 3, 6, 2, 3, 2, 6, 6, 4, 4, 5, 9, 7],
        [6, 0, 8, 3, 2, 6, 8, 4, 8, 8, 13, 7, 5, 8, 12, 10, 14],
        [9, 8, 0, 11, 10, 6, 3, 9, 5, 8, 4, 15, 14, 13, 9, 18, 9],
        [8, 3, 11, 0, 1, 7, 10, 6, 10, 10, 14, 6, 7, 9, 14, 6, 16],
        [7, 2, 10, 1, 0, 6, 9, 4, 8, 9, 13, 4, 6, 8, 12, 8, 14],
        [3, 6, 6, 7, 6, 0, 2, 3, 2, 2, 7, 9, 7, 7, 6, 12, 8],
        [6, 8, 3, 10, 9, 2, 0, 6, 2, 5, 4, 12, 10, 10, 6, 15, 5],
        [2, 4, 9, 6, 4, 3, 6, 0, 4, 4, 8, 5, 4, 3, 7, 8, 10],
        [3, 8, 5, 10, 8, 2, 2, 4, 0, 3, 4, 9, 8, 7, 3, 13, 6],
        [2, 8, 8, 10, 9, 2, 5, 4, 3, 0, 4, 6, 5, 4, 3, 9, 5],
        [6, 13, 4, 14, 13, 7, 4, 8, 4, 4, 0, 10, 9, 8, 4, 13, 4],
        [6, 7, 15, 6, 4, 9, 12, 5, 9, 6, 10, 0, 1, 3, 7, 3, 10],
        [4, 5, 14, 7, 6, 7, 10, 4, 8, 5, 9, 1, 0, 2, 6, 4, 8],
        [4, 8, 13, 9, 8, 7, 10, 3, 7, 4, 8, 3, 2, 0, 4, 5, 6],
        [5, 12, 9, 14, 12, 6, 6, 7, 3, 3, 4, 7, 6, 4, 0, 9, 2],
        [9, 10, 18, 6, 8, 12, 15, 8, 13, 9, 13, 3, 4, 5, 9, 0, 9],
        [7, 14, 9, 16, 14, 8, 5, 10, 6, 5, 4, 10, 8, 6, 2, 9, 0],
    ]
    data['time_windows'] = [
        (0, 30),  # depot
        (0, 30),  # 1
        (0, 30),  # 2
        (0, 30),  # 3
        (0, 30),  # 4
        (0, 30),  # 5
        (0, 30),  # 6
        (0, 30),  # 7
        (0, 30),  # 8
        (0, 30),  # 9
        (0, 30),  # 10
        (0, 30),  # 11
        (0, 30),  # 12
        (0, 30),  # 13
        (0, 30),  # 14
        (0, 30),  # 15
        (0, 30),  # 16
    ]
    data['num_vehicles'] = 4
    data['depot'] = 0
    data['demands'] = [0, 1, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
    data['vehicle_capacities'] = [45, 45, 45, 45]
    data['weight'] = [0, 1, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
    data['vehicle_weight_fit'] = [45, 45, 45, 45]
    data['allow_return'] = True
    data['starts'] = [1, 2, 15, 16]
    data['ends'] = [0, 0, 0, 0]
    # data['starts'] = []
    # data['ends'] = []
    # if end_loc for the vehicle is None -> use start_loc and reduce
    data["start_end"] = [data['starts'], data['ends']] if data['starts'] != [] else [
        data['depot']]  # if id of end_locs are the same -> ['depot']

    data['vehicle_unload_time'] = 5
    data['depot_capacity'] = 2
    data['pickups_deliveries'] = [
        [3, 4],
    ]
    data['pickups_delivery_alternatives'] = [
        [[3, 4], [1]]
    ]
    # [node_id, vehicle_id]
    data['allowed_vehicles'] = {
        7: [1],
        2: [1, 3]
    }

    return data


async def main(_data):
    """Solve the CVRP problem."""
    print("Solve the CVRP problem")
    # data = create_data_model() # Instantiate the test data model.
    data = _data._data
    order = _data._order
    driver = _data._driver
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)
    solver = routing.solver()

    """Add Distance constraint"""
    print("Add Distance constraint")

    # Add Capacity constraint
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return order['capacity'][from_node]


    """Add Capacity constraint"""
    print("Add Capacity constraint")
    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    print(".AddDimensionWithVehicleCapacity")
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')


    # Add weight constraint
    def weight_callback(from_index):
        """Returns the weight of the node."""
        # Convert from routing variable Index to weight NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return order['weight'][from_node]


    """Add weight constraint"""
    print("Add weight constraint")
    weight_callback_index = routing.RegisterUnaryTransitCallback(weight_callback)
    routing.AddDimensionWithVehicleCapacity(
        weight_callback_index,
        0,
        data['vehicle_weights'],
        True,
        'Weight')

    """Time Callback"""
    print("Time Callback")


    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]


    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        data['max_horizon'],  # allow waiting time
        data['max_horizon'] * 10,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(order['time_window']):
        if location_idx == 0 or not time_window: continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
        routing.AddToAssignment(time_dimension.SlackVar(index))

    """Add time window constraints for each vehicle start node."""
    print("Add time window constraints for each vehicle start node")
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        routing.AddToAssignment(time_dimension.SlackVar(index))

    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))

    """Pickup and Delivery"""
    print("Pickup and Delivery")
    for request in order['pickups_deliveries']:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(
            routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index))
        routing.solver().Add(
            time_dimension.CumulVar(pickup_index) <= time_dimension.CumulVar(delivery_index))

    """Car Type"""
    print("Car Type")
    # for order_index in data['allowed_vehicles']:
    #     routing.SetAllowedVehiclesForIndex(data['allowed_vehicles'][order_index], manager.NodeToIndex(order_index))

    print("""~~~~~~~~~~~~~~~~~ SOLVE ~~~~~~~~~~~~~~~~~""")
    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)  # PATH_CHEAPEST_ARC) # PARALLEL_CHEAPEST_INSERTION
    # search_parameters.log_search = True

    # Solve the problem.
    print("Solve the problem")
    assignment = routing.SolveWithParameters(search_parameters)
    # Print the soltion
    print("Print the soltion")
    solution = {}
    if assignment:
        print_solution(data, manager, routing, assignment)
        solution = to_dict(_data, manager, routing, assignment)
        return solution


#     https://github.com/google/or-tools/blob/master/examples/python/cvrptw_plot.py#L641

if __name__ == '__main__':
    main()
