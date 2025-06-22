from flight import Flight  # Assuming Flight is defined elsewhere


class Queue:
    def __init__(self):
        self.queue = [None] * 2
        self._front = 0  # Renamed from `head`
        self._end = 0    # Renamed from `tail`
        self._current_size = 0  # Renamed from `size`

    def push(self, item):
        if self._current_size == len(self.queue):
            # Resize logic
            new_capacity = len(self.queue) * 2
            expanded_queue = [None] * new_capacity
            idx = 0
            while idx < self._current_size:
                expanded_queue[idx] = self.queue[(self._front + idx) % len(self.queue)]
                idx += 1
            self.queue = expanded_queue
            self._front = 0
            self._end = self._current_size

        self.queue[self._end] = item
        self._end = (self._end + 1) % len(self.queue)
        self._current_size += 1

    def pop(self):
        if self._current_size <= 0:
            raise IndexError("Queue is empty")

        result = self.queue[self._front]
        self.queue[self._front] = None  # Clearing for garbage collection
        self._front = (self._front + 1) % len(self.queue)
        self._current_size -= 1
        return result

    def is_empty(self):
        return self._current_size <= 0

    def __len__(self):
        return self._current_size


class Heap:
    def __init__(self, comparison_fn=lambda a, b: a[0] < b[0], elements=[]):
        self.comparison_fn = comparison_fn
        self.heap_list = list(elements)
        _n = len(self.heap_list)
        idx = _n - 1
        while idx >= 0:
            current = idx
            while True:
                left_pos = 2 * current + 1
                right_pos = 2 * current + 2
                swap_with = current
                if left_pos < len(self.heap_list):
                    swap_with = left_pos if self.comparison_fn(self.heap_list[left_pos], self.heap_list[swap_with]) else swap_with
                if right_pos < len(self.heap_list):
                    swap_with = right_pos if self.comparison_fn(self.heap_list[right_pos], self.heap_list[swap_with]) else swap_with
                if swap_with != current:
                    self.heap_list[current], self.heap_list[swap_with] = self.heap_list[swap_with], self.heap_list[current]
                    current = swap_with
                else:
                    break
            idx -= 1

    def insert(self, element):
        self.heap_list.append(element)
        pos = len(self.heap_list) - 1
        while pos > 0:
            parent_pos = (pos - 1) // 2
            if self.comparison_fn(self.heap_list[pos], self.heap_list[parent_pos]):
                self.heap_list[pos], self.heap_list[parent_pos] = self.heap_list[parent_pos], self.heap_list[pos]
                pos = parent_pos
            else:
                break

    def extract(self):
        if len(self.heap_list) <= 0:
            raise IndexError("Heap is empty")

        root_element = self.heap_list[0]
        if len(self.heap_list) > 1:
            self.heap_list[0] = self.heap_list.pop()
            curr = 0
            while curr < len(self.heap_list):
                l_child = 2 * curr + 1
                r_child = 2 * curr + 2
                smallest = curr
                if l_child < len(self.heap_list):
                    smallest = l_child if self.comparison_fn(self.heap_list[l_child], self.heap_list[smallest]) else smallest
                if r_child < len(self.heap_list):
                    smallest = r_child if self.comparison_fn(self.heap_list[r_child], self.heap_list[smallest]) else smallest
                if smallest != curr:
                    self.heap_list[curr], self.heap_list[smallest] = self.heap_list[smallest], self.heap_list[curr]
                    curr = smallest
                else:
                    break
        else:
            self.heap_list.pop()
        return root_element

    def top(self):
        if len(self.heap_list) <= 0:
            raise IndexError("Heap is empty")
        return self.heap_list[0]

    def is_empty(self):
        return len(self.heap_list) <= 0

class Planner:
    """A flight planner that provides route options based on flight data and preferences."""

    def __init__(self, flights):
        """Initialize the planner with flight data and build a graph of connections."""
        self.flights = flights
        self.max_city_no = self._find_max_city_no()
        self.graph = self._initialize_graph(len(flights))
        self.city_departures = self._initialize_city_departures(self.max_city_no)
        self.build_graph()

    def _find_max_city_no(self):
        """Find the maximum city number in the flights data."""
        max_city = 0
        for flight in self.flights:
            if flight.start_city > max_city:
                max_city = flight.start_city
            if flight.end_city > max_city:
                max_city = flight.end_city
        return max_city

    def _initialize_graph(self, num_flights):
        """Initialize an empty graph structure for flights."""
        graph = []
        for _ in range(num_flights):
            graph.append([])
        return graph

    def _initialize_city_departures(self, max_city_no):
        """Initialize an empty list structure to store city departures."""
        city_departures = []
        for _ in range(max_city_no + 1):
            city_departures.append([])
        return city_departures

    def build_graph(self):
        """Build a graph representing all valid connections between flights."""
        self._populate_city_departures()
        self._create_edges_between_flights()

    def _populate_city_departures(self):
        """Populate the city_departures list with flight indices based on start_city."""
        for i in range(len(self.flights)):
            flight = self.flights[i]
            self.city_departures[flight.start_city].append(i)

    def _create_edges_between_flights(self):
        """Create graph edges based on flight connections and layover conditions."""
        for i in range(len(self.flights)):
            flight = self.flights[i]
            for next_flight_index in self.city_departures[flight.end_city]:
                next_flight = self.flights[next_flight_index]
                if self._has_valid_layover(flight, next_flight):
                    self.graph[i].append(next_flight_index)

    def _has_valid_layover(self, flight, next_flight):
        """Check if the next flight has a valid layover time from the current flight."""
        return next_flight.departure_time >= flight.arrival_time + 20

    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying:
        The route has the least number of flights, and within routes with same number of flights,
        arrives the earliest.
        """
        if start_city == end_city:
            return []

        queue = Queue()
        parent = [None] * len(self.flights)
        visited = [False] * len(self.flights)
        least_flights = float('inf')
        earliest_arrival = float('inf')
        best_flight_index = None

        self._initialize_queue(queue, visited, start_city, t1)

        while not queue.is_empty():
            current_index, flights_count, current_time = queue.pop()
            flight = self.flights[current_index]

            if self._reached_destination(flight, end_city, current_time, t2, flights_count, least_flights, earliest_arrival):
                least_flights = flights_count
                earliest_arrival = current_time
                best_flight_index = current_index

            self._explore_connections(queue, current_index, flights_count, current_time, visited, parent)

        return self._reconstruct_route(best_flight_index, parent)

    def _initialize_queue(self, queue, visited, start_city, t1):
        """Initialize the BFS queue with flights from the start city that meet the departure time condition."""
        for i in range(len(self.flights)):
            flight = self.flights[i]
            if flight.start_city == start_city and flight.departure_time >= t1:
                queue.push((i, 1, flight.arrival_time))
                visited[i] = True

    def _reached_destination(self, flight, end_city, current_time, t2, flights_count, least_flights, earliest_arrival):
        """Check if the current flight reaches the destination under the route constraints."""
        return flight.end_city == end_city and current_time <= t2 and (
            flights_count < least_flights or (flights_count == least_flights and current_time < earliest_arrival))

    def _explore_connections(self, queue, current_index, flights_count, current_time, visited, parent):
        """Explore valid connections to the next flights."""
        for next_flight_index in self.graph[current_index]:
            next_flight = self.flights[next_flight_index]
            if next_flight.departure_time >= current_time + 20 and not visited[next_flight_index]:
                parent[next_flight_index] = current_index
                visited[next_flight_index] = True
                queue.push((next_flight_index, flights_count + 1, next_flight.arrival_time))

    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying:
        The route is a cheapest route
        """
        if start_city == end_city:
            return []

        min_fare = [float('inf')] * len(self.flights)
        min_heap = Heap(comp)
        parent = [None] * len(self.flights)
        best_flight_index = None

        self._initialize_dijkstra(min_heap, min_fare, start_city, t1)

        while not min_heap.is_empty():
            current_fare, current_index, current_time = min_heap.extract()
            flight = self.flights[current_index]

            if self._is_cheapest_route_to_destination(flight, end_city, current_time, t2):
                best_flight_index = current_index
                break

            self._update_min_fare_connections(min_heap, current_index, current_fare, current_time, min_fare, parent)

        return self._reconstruct_route(best_flight_index, parent)

    def _initialize_dijkstra(self, min_heap, min_fare, start_city, t1):
        """Initialize the min-heap and fare list for Dijkstra's algorithm."""
        for i in range(len(self.flights)):
            flight = self.flights[i]
            if flight.start_city == start_city and flight.departure_time >= t1:
                min_fare[i] = flight.fare
                min_heap.insert((flight.fare, i, flight.arrival_time))

    def _is_cheapest_route_to_destination(self, flight, end_city, current_time, t2):
        """Check if the flight reaches the destination within the time constraint."""
        return flight.end_city == end_city and current_time <= t2

    def _update_min_fare_connections(self, min_heap, current_index, current_fare, current_time, min_fare, parent):
        """Update connections with new minimum fares."""
        for next_flight_index in self.graph[current_index]:
            next_flight = self.flights[next_flight_index]
            new_fare = current_fare + next_flight.fare
            if next_flight.departure_time >= current_time + 20 and new_fare < min_fare[next_flight_index]:
                min_fare[next_flight_index] = new_fare
                parent[next_flight_index] = current_index
                min_heap.insert((new_fare, next_flight_index, next_flight.arrival_time))

    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying:
        The route has the least number of flights, and within routes with same number of flights,
        is the cheapest
        """
        if start_city == end_city:
            return []

        min_cost_with_flights = [(float('inf'), float('inf'))] * len(self.flights)
        min_heap = Heap(comp_length_then_fare)
        parent = [None] * len(self.flights)
        best_flight_index = None

        self._initialize_least_flights_dijkstra(min_heap, min_cost_with_flights, start_city, t1)

        while not min_heap.is_empty():
            flights_count, current_cost, current_index, current_time = min_heap.extract()
            flight = self.flights[current_index]

            if self._is_cheapest_route_to_destination(flight, end_city, current_time, t2):
                best_flight_index = current_index
                break

            self._update_least_flights_cost_connections(min_heap, current_index, flights_count, current_cost, current_time, min_cost_with_flights, parent)

        return self._reconstruct_route(best_flight_index, parent)

    def _initialize_least_flights_dijkstra(self, min_heap, min_cost_with_flights, start_city, t1):
        """Initialize the min-heap for least flights cheapest route algorithm."""
        for i in range(len(self.flights)):
            flight = self.flights[i]
            if flight.start_city == start_city and flight.departure_time >= t1:
                min_cost_with_flights[i] = (1, flight.fare)
                min_heap.insert((1, flight.fare, i, flight.arrival_time))

    def _update_least_flights_cost_connections(self, min_heap, current_index, flights_count, current_cost, current_time, min_cost_with_flights, parent):
        """Update connections with minimum cost and flights constraints."""
        for next_flight_index in self.graph[current_index]:
            next_flight = self.flights[next_flight_index]
            new_cost = current_cost + next_flight.fare
            new_flights_count = flights_count + 1

            if next_flight.departure_time >= current_time + 20:
                if (new_flights_count < min_cost_with_flights[next_flight_index][0] or
                    (new_flights_count == min_cost_with_flights[next_flight_index][0] and
                     new_cost < min_cost_with_flights[next_flight_index][1])):
                    min_cost_with_flights[next_flight_index] = (new_flights_count, new_cost)
                    parent[next_flight_index] = current_index
                    min_heap.insert((new_flights_count, new_cost, next_flight_index, next_flight.arrival_time))

    def _reconstruct_route(self, flight_index, parent):
        """Reconstruct the route from the end flight back to the start flight."""
        route = []
        while flight_index is not None:
            route.append(self.flights[flight_index])
            flight_index = parent[flight_index]
        route.reverse()
        return route
