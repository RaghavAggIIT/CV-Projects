from flight import Flight
from planner import Planner

def main():
    flights = [
        Flight(0, 0, 0, 1, 10, 10000),      # City 0 to 1
        Flight(1, 0, 0, 1, 40, 5000),       # City 0 to 3
        Flight(2, 1, 30, 2, 40, 5000),       # City 1 to 2
        Flight(3, 1, 70, 2, 80, 15000),   # City 1 to 2
    ]
    
    flight_planner = Planner(flights)
    
    # The three tasks
    # route1 = flight_planner.least_flights_ealiest_route(0, 3, 0, 300)
    route2 = flight_planner.cheapest_route(0, 2, 0, 300)
    # route2 = flight_planner.least_flights_cheapest_route(0, 2, 0, 300)
    
    # expected output
    expected_route2 = [flights[0], flights[2]]  # 0-1-2-4, 270 fare
    
    # Print the expected route and the actual route
    print("Expected Route:")
    for flight in expected_route2:
        print(f"Flight No: {flight.flight_no}, Start City: {flight.start_city}, "
              f"Departure Time: {flight.departure_time}, End City: {flight.end_city}, "
              f"Arrival Time: {flight.arrival_time}, Fare: {flight.fare}")
    
    print("\nActual Route:")
    for flight in route2:
        print(f"Flight No: {flight.flight_no}, Start City: {flight.start_city}, "
              f"Departure Time: {flight.departure_time}, End City: {flight.end_city}, "
              f"Arrival Time: {flight.arrival_time}, Fare: {flight.fare}")
    
    if route2 == expected_route2:
        print("\nTask 2 PASSED")

if __name__ == "__main__":
    main()