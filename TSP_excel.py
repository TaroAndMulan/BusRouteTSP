from database_operation import get_customer_byID
from itertools import product
from mip import Model, xsum, minimize, BINARY, OptimizationStatus
from math import radians, sin, cos, sqrt, atan2
import json
import logging


def validate_coordinates(coordinates):
    for coord in coordinates:
        if len(coord) != 2:
            raise ValueError(f"Invalid coordinate: {coord}")
        if not all(isinstance(c, (int, float)) for c in coord):
            raise ValueError(
                f"Coordinate contains non-numeric values: {coord}")



def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat /
            2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def calculate_distance_matrix(coordinates):
    n = len(coordinates)
    dists = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            lat1, lon1 = coordinates[i]
            lat2, lon2 = coordinates[j]
            dist = haversine(lat1, lon1, lat2, lon2)
            dists[i][j] = dists[j][i] = dist
    return dists


logging.basicConfig(level=logging.DEBUG)


def solve_tsp(places, coordinates):
    # Define the starting point
    start_point = [13.74164416, 100.0839788]
    # Add the starting point to coordinates
    coordinates = [start_point] + coordinates
    #print ("inside solve ", coordinates)
    places = ['Start'] + places  # Add 'Start' as the first place
    # Calculate the distance matrix including the starting point
    dists = calculate_distance_matrix(coordinates)
    #print ("matrisx ", dists)
    n, V = len(dists), set(range(len(dists)))

    c = dists
    # Initialize the model
    model = Model()
    x = [[model.add_var(var_type=BINARY) for j in V] for i in V]
    y = [model.add_var() for i in V]

    model.objective = minimize(xsum(c[i][j] * x[i][j] for i in V for j in V))

    def add_constraints(model, x, y, n, V):
        for i in V:
            model += xsum(x[i][j] for j in V - {i}) == 1

        for i in V:
            model += xsum(x[j][i] for j in V - {i}) == 1

        for (i, j) in product(V - {0}, V - {0}):
            if i != j:
                model += y[i] - (n + 1) * x[i][j] >= y[j] - n

    # Add constraints and optimize
    add_constraints(model, x, y, n, V)
    model.verbose = 0
    model.optimize()

    if model.status == OptimizationStatus.OPTIMAL:
        logging.debug(f"Optimal solution found: {model.objective_value}")
    else:
        logging.debug(f"Model status: {model.status}")
        print("No feasible solution found.")

    # Extract route
    route = []
    if model.status == OptimizationStatus.OPTIMAL:
        route.append(places[0])
        nc = 0
        while True:
            nc = [i for i in V if x[nc][i].x >= 0.99][0]
            route.append(places[nc])
            if nc == 0:
                break
        print ("route from TSP SOLVER IS : ", route)
        # Output route
        return route
        """
        # Save route to JSON
        with open('route.json', 'w') as f:
            json.dump({'route': route, 'coordinates': coordinates}, f)
        """
    else:
        print("No feasible solution found.")
        print("Model status:", model.status)


def CalculateRoutesExcel(places,coordinates):

    if not places or not coordinates:
        print("No data found")
        return

    validate_coordinates(coordinates)
    return solve_tsp(places, coordinates)
