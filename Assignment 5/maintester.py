import time
from flight import Flight
from planner import Planner

def load_flights_from_file(filename):
    flights = []
    with open(filename, 'r') as file:
        n = int(file.readline().strip())  # Number of flights
        
        # Read each flight's data
        for _ in range(n):
            flight_data = file.readline().strip().split()
            flight_no = int(flight_data[0])
            start_city = int(flight_data[1])
            departure_time = int(flight_data[2])
            end_city = int(flight_data[3])
            arrival_time = int(flight_data[4])
            fare = int(flight_data[5])
            flights.append(Flight(flight_no, start_city, departure_time, end_city, arrival_time, fare))
        
        # Read the start city, end city, t1, and t2 after flights data
        start_city, end_city, t1, t2 = map(int, file.readline().strip().split())
    
    return flights, start_city, end_city, t1, t2

def format_route(route):
    """Helper function to format the route for easy reading."""
    if not route:
        return "No route found"
    route_details = []
    for flight in route:
        route_details.append(f"Flight {flight.flight_no}: {flight.start_city} -> {flight.end_city} "
                             f"Depart: {flight.departure_time} Arrive: {flight.arrival_time} Fare: {flight.fare}")
    return "\n".join(route_details)

def main():
    # Load flights and route parameters from file
    flights, start_city, end_city, t1, t2 = load_flights_from_file('flights.txt')
    
    # Create a flight planner instance
    flight_planner = Planner(flights)
    
    # Open output file
    with open('output.txt', 'w') as output_file:
        # # Calculate routes based on the three tasks and record the time taken
        start_time = time.time()
        route1 = flight_planner.least_flights_earliest_route(start_city, end_city, t1, t2)
        route1_time = time.time() - start_time
        
        start_time = time.time()
        route2 = flight_planner.cheapest_route(start_city, end_city, t1, t2)
        route2_time = time.time() - start_time
        
        start_time = time.time()
        route3 = flight_planner.least_flights_cheapest_route(start_city, end_city, t1, t2)
        route3_time = time.time() - start_time
        

        output_file.write("Route 1: Least Flights, Earliest Arrival\n")
        output_file.write(format_route(route1) + "\n")
        print(f"Time taken: {route1_time:.4f} seconds\n\n")
        
        output_file.write("Route 2: Cheapest Route\n")
        output_file.write(format_route(route2) + "\n")
        print(f"Time taken: {route2_time:.4f} seconds\n\n")
        
        output_file.write("Route 3: Least Flights, Cheapest Route\n")
        output_file.write(format_route(route3) + "\n")
        print(f"Time taken: {route3_time:.4f} seconds\n")

if __name__ == "__main__":
    main()
