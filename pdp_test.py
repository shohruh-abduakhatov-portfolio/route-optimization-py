"""Vehicles Routing Problem (VRP)."""

from __future__ import print_function

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

from helper import *


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = [[0, 28, 29],
                               [28, 0, 23],
                               [29, 20, 0]]
    data['time_matrix'] = [[0, 56, 59],
                           [56, 0, 46],
                           [58, 40, 0]]
    data['time_windows'] = [
        None,
        [1579016931, 1579019931],
        [1579042133, 1579092133]
    ]
    data['num_vehicles'] = 2
    data['depot'] = 0
    data['demands'] = [0, 1, 1]
    data['vehicle_capacities'] = [100, 100]
    data['weight'] = [0, 2, 2]
    data['vehicle_weight_fit'] = [1000, 1000]
    data['allow_return'] = False
    data['starts'] = [1, 2, 15, 16]
    data['ends'] = [0, 0, 0, 0]
    data['horizon'] = 1579092133
    data['pickups_deliveries'] = [
        [1, 2]
    ]
    # [node_id, vehicle_id]
    data['allowed_vehicles'] = {
        7: [1],
        2: [1, 3]
    }

    return data


def main():
    """Solve the CVRP problem."""
    data = create_data_model()  # Instantiate the test data model.
    # data = _data._data
    # order = _data._order
    # driver = _data._driver
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)
    solver = routing.solver()

    """Add Distance constraint"""


    # Add Capacity constraint
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]


    """Add Capacity constraint"""
    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
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
        return data['weight'][from_node]


    """Add weight constraint"""
    weight_callback_index = routing.RegisterUnaryTransitCallback(weight_callback)
    routing.AddDimensionWithVehicleCapacity(
        weight_callback_index,
        0,
        data['vehicle_weight_fit'],
        True,
        'Weight')

    """Time Callback"""


    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]*60


    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        data['horizon'],  # allow waiting time
        data['horizon'] * 10,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == 0 or not time_window:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
        # time_dimension.SetCumulVarSoftLowerBound(index, time_window[0], 1)
        # time_dimension.SetCumulVarSoftUpperBound(index, time_window[1], 1)
        routing.AddToAssignment(time_dimension.SlackVar(index))

    """Add time window constraints for each vehicle start node."""
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        routing.AddToAssignment(time_dimension.SlackVar(index))

    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))

    """Pickup and Delivery"""
    for request in data['pickups_deliveries']:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(
            routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index))
        routing.solver().Add(
            time_dimension.CumulVar(pickup_index) <= time_dimension.CumulVar(delivery_index))

    # """Car Type"""
    # for order_index in data['allowed_vehicles']:
    #     routing.SetAllowedVehiclesForIndex(data['allowed_vehicles'][order_index], manager.NodeToIndex(order_index))

    print("""~~~~~~~~~~~~~~~~~ SOLVE ~~~~~~~~~~~~~~~~~""")
    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)  # PATH_CHEAPEST_ARC) # PARALLEL_CHEAPEST_INSERTION
    # search_parameters.log_search = True

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)
    # Print the soltion
    solution = {}
    if assignment:
        print_solution(data, manager, routing, assignment)
        # solution = to_dict(data, manager, routing, assignment)

    print('no solution')


#     https://github.com/google/or-tools/blob/master/examples/python/cvrptw_plot.py#L641

if __name__ == '__main__':
    main()
