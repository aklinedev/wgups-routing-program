from driver import Driver
from truck import Truck
from fleet import Fleet
from data_loader import load_packages, load_distance_data
from package_scheduler import build_load
from routing import run_route, _calculate_travel_time
from package import PackageStatus
from reporting import display_package, display_all_packages


# Constants / program data --------------------------------------------------------

PACKAGE_FILE = "data/WGUPS Package File.xlsx"
DISTANCE_FILE = "data/WGUPS Distance Table.xlsx"

HUB = "HUB"

# The actual value represents minutes after midnight
START_TIME = 480        # 8:00 AM
DELAYED_TIME = 545      # 9:05 AM
ADDRESS_FIX_TIME = 620  # 10:20 AM

TRUCK_CAPACITY = 16

# Load data --------------------------------------------------------

packages = load_packages(PACKAGE_FILE)

address_mapping, distance_matrix = load_distance_data(
    DISTANCE_FILE
)

# Create drivers --------------------------------------------------------

driver_1 = Driver(1)
driver_2 = Driver(2)

drivers = [
    driver_1,
    driver_2
]

# Create trucks --------------------------------------------------------

truck_1 = Truck(
    id=1,
    capacity=TRUCK_CAPACITY,
    current_location=HUB
)

truck_2 = Truck(
    id=2,
    capacity=TRUCK_CAPACITY,
    current_location=HUB
)

truck_3 = Truck(
    id=3,
    capacity=TRUCK_CAPACITY,
    current_location=HUB
)

trucks = [
    truck_1,
    truck_2,
    truck_3
]

# Create fleet --------------------------------------------------------

fleet = Fleet(
    drivers,
    trucks,
    START_TIME
)

# This is for package #9 correction --------------------------------------------------------

def correct_package_9():
    package_9 = packages.get(9)

    package_9.address = "410 S State St"
    package_9.city = "Salt Lake City"
    package_9.state = "UT"
    package_9.zip_code = "84111"
    package_9.address_corrected_at = ADDRESS_FIX_TIME
    package_9.address_is_valid = True

# Time event helper --------------------------------------------------------
# This checks whether the simulation has reached a
# time where something in the data should change
def apply_time_events(current_time):

    # Move delayed packages to the hub once
    # their availability time has been reached.
    for package in packages:

        if (
            package.status == PackageStatus.DELAYED
            and package.available_at is not None
            and current_time >= package.available_at
        ):
            package.status = PackageStatus.AT_HUB


    # Package #9 address correction.
    package_9 = packages.get(9)

    if (
        current_time >= ADDRESS_FIX_TIME
        and not package_9.address_is_valid
    ):
        correct_package_9()

# Delivery check helper --------------------------------------------------------
# This helper loops through every package and checks its status.
# It returns True is all packages are deliverd, and False otherwise.
def all_packages_delivered():
    for package in packages:
        if package.status != PackageStatus.DELIVERED:
            return False

    return True

# Truck helper --------------------------------------------------------

def prepare_and_dispatch(truck, driver, departure_time):

    apply_time_events(departure_time)

    load = build_load(
        packages,
        truck,
        departure_time
    )

    if not load:
        return None

    truck.load_multiple_packages(load)

    if not fleet.dispatch(
        driver,
        truck,
        departure_time
    ):
        return None

    finish_time = run_route(
        truck,
        address_mapping,
        distance_matrix
    )

    return finish_time

# Return truck to hub --------------------------------------------------------

def return_truck_to_hub(truck, driver, current_time):

    hub_index = address_mapping[HUB]
    truck_index = address_mapping[truck.current_location]

    return_distance = distance_matrix[
        truck_index
    ][
        hub_index
    ]

    return_time = (
        current_time
        + _calculate_travel_time(return_distance)
    )

    truck.add_mileage(return_distance)

    fleet.return_to_hub(
        driver,
        truck,
        return_time,
        HUB
    )

    return return_time

# First two trucks --------------------------------------------------------

load_1 = build_load(
    packages,
    truck_1,
    START_TIME
)

truck_1.load_multiple_packages(load_1)

fleet.dispatch(
    driver_1,
    truck_1,
    START_TIME
)

apply_time_events(DELAYED_TIME)


load_2 = build_load(
    packages,
    truck_2,
    DELAYED_TIME
)

truck_2.load_multiple_packages(load_2)

fleet.dispatch(
    driver_2,
    truck_2,
    DELAYED_TIME
)

# Run the initial routes --------------------------------------------------------

truck_1_finish = run_route(
    truck_1,
    address_mapping,
    distance_matrix
)

truck_2_finish = run_route(
    truck_2,
    address_mapping,
    distance_matrix
)

# Return first two trucks --------------------------------------------------------

truck_1_return = return_truck_to_hub(
    truck_1,
    driver_1,
    truck_1_finish
)

truck_2_return = return_truck_to_hub(
    truck_2,
    driver_2,
    truck_2_finish
)

# Determine which driver becomes available first --------------------------------------------------------

if truck_1_return <= truck_2_return:
    available_driver = driver_1
    next_departure = truck_1_return
else:
    available_driver = driver_2
    next_departure = truck_2_return

# Remaining deliveries --------------------------------------------------------

current_time = next_departure
while not all_packages_delivered():

    # Apply any time-based changes before trying to build another load.
    apply_time_events(current_time)

    selected_truck = None
    load = None

    # Try each truck until one can take a valid load.
    for truck in trucks:

        possible_load = build_load(
            packages,
            truck,
            current_time
        )

        if possible_load:
            selected_truck = truck
            load = possible_load
            break


    # If nothing can currently be loaded,
    # move forward to the next important event.
    if not load:

        if current_time < DELAYED_TIME:
            current_time = DELAYED_TIME
            continue

        if current_time < ADDRESS_FIX_TIME:
            current_time = ADDRESS_FIX_TIME
            continue

        print("Packages remain, but no eligible load could be built.")
        break

    selected_truck.load_multiple_packages(load)


    if not fleet.dispatch(
        available_driver,
        selected_truck,
        current_time
    ):
        print("Unable to dispatch truck.")
        break

    finish_time = run_route(
        selected_truck,
        address_mapping,
        distance_matrix
    )

    # If the final package was delivered,
    # the simulation ends without returning to the hub.
    if all_packages_delivered():
        final_time = finish_time
        break

    # Packages still remain, so return to the hub
    # and prepare for another trip.
    current_time = return_truck_to_hub(
        selected_truck,
        available_driver,
        finish_time
    )

# Results --------------------------------------------------------

total_mileage = sum(
    truck.mileage
    for truck in trucks
)

print(f"Total mileage: {total_mileage:.1f}")

delivered_count = 0
for package in packages:
    if package.status == PackageStatus.DELIVERED:
        delivered_count += 1
    else:
        print(
            f"NOT DELIVERED: Package {package.id}"
        )


print(
    f"Delivered packages: "
    f"{delivered_count}/40"
)

# Supervisor methods --------------------------------------------------------

def get_query_time():
    while True:
        time_input = input("Enter query time (HH:MM, 24-hour format): ").strip()

        try:
            hours, minutes = map(int, time_input.split(":"))
            if (
                0 <= hours <= 23
                and 0 <= minutes <= 59
            ):
                return hours * 60 + minutes

            print("Invalid time. Please enter a valid time.")

        except ValueError:
            print("Invalid format. Example: 10:20 or 13:12")


def run_tracking_interface():

    while True:
        print("\n========== WGUPS PACKAGE TRACKING ==========")
        print("1. Look up a package")
        print("2. View all packages")
        print("3. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":

            try:
                package_id = int(input("Enter package ID: "))
            except ValueError:
                print("Please enter a valid package ID.")
                continue

            package = packages.get(package_id)

            if package is None:
                print(f"Package {package_id} was not found.")
                continue

            query_time = get_query_time()

            display_package(package, query_time)

        elif choice == "2":

            query_time = get_query_time()

            display_all_packages(
                packages,
                query_time
            )

        elif choice == "3":
            print("Exiting package tracking.")
            break

        else:
            print("Invalid selection. Please choose 1, 2, or 3.")


# Start supervisor interface --------------------------------------------------

run_tracking_interface()