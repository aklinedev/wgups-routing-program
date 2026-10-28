class Truck:
    def __init__(
        self,
        id,
        capacity,
        current_location,
        departure_time=None,
        return_time=None
    ):
        self.id = id
        self.capacity = capacity
        self.packages = []
        self.mileage = 0
        self.current_location = current_location
        self.departure_time = departure_time
        self.return_time = return_time

    def is_full(self):
        # Using >= provides a little more saftey over == , in the case
        # length passes capacity.
        return len(self.packages) >= self.capacity
        
    def load_package(self, package):
        if not self.is_full():
            self.packages.append(package)
            return True
        else:
            return False

    def load_multiple_packages(self, packages):
        # Keeping track of packages added, in case max capacity is
        # reached before all packages get loaded.
        packages_added = 0

        for package in packages:
            if not self.load_package(package):
                break
            packages_added += 1

        return packages_added
    
    def remove_package(self, package):
        # Checking before removing, to prevent an exception being thrown
        # in the case it is not there.
        if package in self.packages:
            self.packages.remove(package)
            return True

        return False

    def depart(self, time):
        self.departure_time = time

    def return_to_hub(self, time, hub_loacation):
        self.return_time = time
        self.current_location = hub_loacation

    def add_mileage(self, mileage):
        self.mileage += mileage

    def update_location(self, location):
        self.current_location = location

    def get_remaining_capacity(self):
        return self.capacity - len(self.packages)
