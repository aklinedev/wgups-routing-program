from driver import Driver
from truck import Truck

class Fleet:
    def __init__(self, drivers, trucks, earliest_departure_time):
        self.drivers = drivers
        self.trucks = trucks
        self.earliest_departure_time = earliest_departure_time
        # Assignments here represent the relationship between a driver
        # and a truck.
        self.assignments = {}

    # Using this as an internal implementation method to help
    # simplify the overall logic.
    def _assign_driver_to_truck(self, driver, truck):
        # Before assigning, we check if the driver and truck belong in this
        # fleet. If so, we make sure they are available, then add to dict.
        if driver not in self.drivers:
            return False

        if not self.is_driver_available(driver):
            return False

        if truck not in self.trucks:
            return False

        if not self.is_truck_available(truck):
            return False

        self.assignments[driver.id] = truck
        return True


    def is_driver_available(self, driver):
        return driver.id not in self.assignments
    

    def is_truck_available(self, truck):
        return truck not in self.assignments.values()


    def dispatch(self, driver, truck, time):
        if time < self.earliest_departure_time:
            return False

        # Checking if truck is empty before assingment, to prevent
        # a driver getting assigned an empty truck.
        if not truck.packages:
            return False
        
        if not self._assign_driver_to_truck(driver, truck):
            return False
        
        truck.depart(time)
        for package in truck.packages:
            package.mark_en_route(time)

        return True

    # Helper method used to release a driver and truck from assingments.
    def _release_driver(self, driver, truck):
        if driver.id not in self.assignments:
            return False

        if truck != self.assignments[driver.id]:
            return False
        
        del self.assignments[driver.id]
        return True
        
    # Returns a truck to the hub and releases driver. Assumes truck
    # is empty for this project.
    def return_to_hub(self, driver, truck, time, hub_location):
        if self._release_driver(driver, truck):
            truck.return_to_hub(time, hub_location)
            return True
        return False