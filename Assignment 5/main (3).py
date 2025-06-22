from flight import Flight
from planner import Planner

def main():

    
    flights = [
        Flight(0, 0, 480, 1, 540, 100),    # Flight 1: City A(0) -> B(1), 8:00-9:00, cost 100
        Flight(1, 1, 550, 2, 600, 200),    # Flight 2: City B(1) -> C(2), 9:10-10:00, cost 200
        Flight(2, 0, 490, 1, 550, 150),    # Flight 3: City A(0) -> B(1), 8:10-9:10, cost 150
        Flight(3, 1, 600, 2, 660, 100)     # Flight 4: City B(1) -> C(2), 10:00-11:00, cost 100
    ]

    # Assume MIN_CONNECTION_TIME is set to 10 minutes (10 time units)
    # Start from city A (0) to city C (2) with t1 = 480 (8:00) and t2 = 660 (11:00)
    start_city = 0
    end_city = 2
    t1 = 480
    t2 = 660
    flight_planner = Planner(flights)

    # Run both versions of the cheapest_route method
    route1 = flight_planner.cheapest_route(start_city, end_city, t1, t2)
    route2 = flight_planner.least_flights_cheapest_route(start_city, end_city, t1, t2)
    # route2 = flight_planner.least_flights_cheapest_route(0, 2, 0, 300)
    
    
    # Print the expected route and the actual route
    
    print("\nActual Route1:")
    for flight in route1:
        print(f"Flight No: {flight.flight_no}, Start City: {flight.start_city}, "
              f"Departure Time: {flight.departure_time}, End City: {flight.end_city}, "
              f"Arrival Time: {flight.arrival_time}, Fare: {flight.fare}")
    

    print("\nActual Route2:")
    for flight in route2:
        print(f"Flight No: {flight.flight_no}, Start City: {flight.start_city}, "
              f"Departure Time: {flight.departure_time}, End City: {flight.end_city}, "
              f"Arrival Time: {flight.arrival_time}, Fare: {flight.fare}")
        
if __name__ == "__main__":
    main()





# from flight import Flight
# from planner import Planner

# def main():
#     flights = [
#         Flight(0, 0, 100, 1, 200, 50),
#         Flight(1, 1, 250, 2, 350, 60),
#         Flight(2, 2, 400, 3, 500, 70),
#         Flight(3, 3, 550, 4, 650, 80),
#         Flight(4, 0, 100, 4, 300, 500),
#         Flight(5, 0, 100, 3, 250, 400),
#         Flight(6, 0, 100, 2, 200, 40),
#         Flight(7, 2, 220, 4, 350, 45),
#         Flight(8, 1, 220, 3, 320, 35),
#         Flight(9, 3, 340, 4, 440, 30),
#         Flight(10, 0, 150, 5, 250, 55),
#         Flight(11, 5, 270, 3, 370, 45),
#         Flight(12, 5, 270, 4, 400, 65),
#         Flight(13, 1, 220, 5, 320, 40),
#         Flight(14, 2, 300, 5, 400, 50),
#         Flight(15, 5, 420, 4, 520, 45),
#         Flight(16, 0, 300, 1, 400, 45),
#         Flight(17, 1, 420, 3, 520, 55),
#         Flight(18, 3, 540, 4, 640, 50),
#         Flight(19, 0, 50, 1, 150, 60),
#         Flight(20, 1, 170, 2, 270, 40),
#         Flight(21, 2, 290, 4, 390, 45),
#         Flight(22, 0, 150, 6, 250, 45),
#         Flight(23, 6, 270, 5, 370, 40),
#         Flight(24, 6, 270, 3, 370, 50),
#         Flight(25, 6, 270, 4, 400, 60),
#         Flight(26, 0, 200, 7, 300, 35),
#         Flight(27, 7, 320, 5, 420, 40),
#         Flight(28, 7, 320, 6, 420, 45),
#         Flight(29, 7, 320, 4, 450, 70),
#     ]
#     # Assume MIN_CONNECTION_TIME is set to 10 minutes (10 time units)
#     # Start from city A (0) to city C (2) with t1 = 480 (8:00) and t2 = 660 (11:00)
#     start_city = 0
#     end_city = 3
#     t1 = 50
#     t2 = 650
#     flight_planner = Planner(flights)

#     # Run both versions of the cheapest_route method
#     route2 = flight_planner.cheapest_route(start_city, end_city, t1, t2)
#     # route2 = flight_planner.least_flights_cheapest_route(start_city, end_city, t1, t2)
#     expected_route2 = [flights[0], flights[8]]  # 0-1-2-4, 270 fare
#     # Print the actual routes
#     print("\nActual Route2:")
#     for flight in route2:
#         print(f"Flight No: {flight.flight_no}, Start City: {flight.start_city}, "
#               f"Departure Time: {flight.departure_time}, End City: {flight.end_city}, "
#               f"Arrival Time: {flight.arrival_time}, Fare: {flight.fare}")
#     print("\nExpected Route2:")
#     for flight in expected_route2:
#         print(f"Flight No: {flight.flight_no}, Start City: {flight.start_city}, "
#               f"Departure Time: {flight.departure_time}, End City: {flight.end_city}, "
#               f"Arrival Time: {flight.arrival_time}, Fare: {flight.fare}")
#     # print("\nActual Route2:")
#     # for flight in route2:
#     #     print(f"Flight No: {flight.flight_no}, Start City: {flight.start_city}, "
#     #           f"Departure Time: {flight.departure_time}, End City: {flight.end_city}, "
#     #           f"Arrival Time: {flight.arrival_time}, Fare: {flight.fare}")

# if __name__ == "__main__":
#     main()






# # from flight import Flight
# # from planner import Planner

# # def main():
# #     flights = [
# #         Flight(0, 0, 0, 1, 10, 10000),
# #         Flight(1, 0, 0, 1, 25, 5000),
# #         Flight(2, 1, 30, 2, 50, 5000),
# #         Flight(3, 1, 60, 2, 70, 15000),
# #     ]
# #     # Assume MIN_CONNECTION_TIME is set to 10 minutes (10 time units)
# #     # Start from city A (0) to city C (2) with t1 = 480 (8:00) and t2 = 660 (11:00)
# #     start_city = 0
# #     end_city = 2
# #     t1 = 0
# #     t2 = 100
# #     flight_planner = Planner(flights)

# #     # Run both versions of the cheapest_route method
# #     route2 = flight_planner.cheapest_route(start_city, end_city, t1, t2)
# #     # route2 = flight_planner.least_flights_cheapest_route(start_city, end_city, t1, t2)
# #     # expected_route2 = [flights[0], flights[8]]  # 0-1-2-4, 270 fare
# #     # Print the actual routes
# #     print("\nActual Route2:")
# #     for flight in route2:
# #         print(f"Flight No: {flight.flight_no}, Start City: {flight.start_city}, "
# #               f"Departure Time: {flight.departure_time}, End City: {flight.end_city}, "
# #               f"Arrival Time: {flight.arrival_time}, Fare: {flight.fare}")
# #     # print("\nExpected Route2:")
# #     # for flight in expected_route2:
# #     #     print(f"Flight No: {flight.flight_no}, Start City: {flight.start_city}, "
# #     #           f"Departure Time: {flight.departure_time}, End City: {flight.end_city}, "
# #     #           f"Arrival Time: {flight.arrival_time}, Fare: {flight.fare}")
# #     # print("\nActual Route2:")
# #     # for flight in route2:
# #     #     print(f"Flight No: {flight.flight_no}, Start City: {flight.start_city}, "
# #     #           f"Departure Time: {flight.departure_time}, End City: {flight.end_city}, "
# #     #           f"Arrival Time: {flight.arrival_time}, Fare: {flight.fare}")

# # if __name__ == "__main__":
# #     main()