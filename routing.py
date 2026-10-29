def _find_closest_package(current_location, packages_on_truck, address_mapping, distance_matrix):
    current_location_index = address_mapping[current_location]

    closest_package = None
    # Sets it to +infinity so any first package always overwrites it.
    closest_distance = float("inf")

    for package in packages_on_truck:
        package_location_index = address_mapping[package.address]
        current_distance = distance_matrix[current_location_index][package_location_index]
        # Keep track of closest package.
        if current_distance < closest_distance:
            closest_distance = current_distance
            closest_package = package
    
    return closest_package, closest_distance


def _calculate_travel_time(distance):
    travel_time = (distance / 18) * 60
    return travel_time

def run_route(truck, address_mapping, distance_matrix):
    current_time = truck.departure_time
    # Goes until the truck is empty.
    while truck.packages:
        # Helper call to find closest package.
        closest_package, closest_distance = _find_closest_package(
            truck.current_location,
            truck.packages,
            address_mapping,
            distance_matrix
        )
        # Update time, mileage, location, and remove package from truck.
        travel_time = _calculate_travel_time(closest_distance)
        current_time += travel_time

        truck.add_mileage(closest_distance)
        truck.update_location(closest_package.address)

        closest_package.mark_delivered(current_time)
        truck.remove_package(closest_package)

    return current_time


