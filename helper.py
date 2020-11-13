def print_solution(data, manager, routing, assignment):
    """Prints assignment on console."""
    print("Prints assignment on console")
    # Display dropped nodes.
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    total_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            time_var = time_dimension.CumulVar(index)
            slack_var = time_dimension.SlackVar(index)

            plan_output += ' [{0}] Time({1},{2})|Slack({3},{4}) -> '.format(
                node_index,
                assignment.Min(time_var),
                assignment.Max(time_var),
                assignment.Min(slack_var),
                assignment.Max(slack_var))

            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        if data['allow_return']:
            time_var = time_dimension.CumulVar(index)
            plan_output += ' [{0}] Time({1},{2}) '.format(
                manager.IndexToNode(index),
                assignment.Min(time_var),
                assignment.Max(time_var))
            total_time += assignment.Min(time_var)

        plan_output += '\n'
        plan_output += 'Distance: {}\n'.format(route_distance)
        print(plan_output)
        total_distance += route_distance

    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total time of all routes: {}min'.format(total_time))


def to_dict(data, manager, routing, assignment):
    solution = {}
    _vehicles = {}
    """Prints assignment on console."""
    print("Prints assignment on console")
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    for vehicle_id in range(data._data['num_vehicles']):
        index = routing.Start(vehicle_id)
        _vehicle = {}
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            time_var = time_dimension.CumulVar(index)
            slack_var = time_dimension.SlackVar(index)
            _vehicle[data._order['id'][node_index]] = {
                "order_id": data._order['order_id'][node_index],
                "time_min": assignment.Min(time_var),
                "time_max": assignment.Max(time_var),
                "slack_min": assignment.Min(slack_var),
                "slack_max": assignment.Max(slack_var),
                "type": data._order['type'][node_index]
            }
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
        if data._data['allow_return']:
            time_var = time_dimension.CumulVar(index)
            node_index = manager.IndexToNode(index)
            _vehicle[data._order['id'][node_index]] = {
                "order_id": data._order['order_id'][node_index],
                "time_min": assignment.Min(time_var),
                "time_max": assignment.Max(time_var),
                "slack_min": assignment.Min(slack_var),
                "slack_max": assignment.Max(slack_var),
                "type": data._order['type'][node_index]
            }
            total_time += assignment.Min(time_var)
        _vehicles[data._driver['id'][vehicle_id]] = {
            'route': _vehicle,
        }
    solution.update({
        "total_time": total_time,
        "solution": _vehicles
    })
    return solution
