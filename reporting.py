from package import PackageStatus

# Returns what the package's status would have been
# at the requested point in simulated time.
def get_status_at_time(package, query_time):

    if (
        package.available_at is not None
        and query_time < package.available_at
    ):
        return PackageStatus.DELAYED

    if package.departure_time is None:
        return PackageStatus.AT_HUB

    if query_time < package.departure_time:
        return PackageStatus.AT_HUB

    if package.delivered_time is None:
        return PackageStatus.EN_ROUTE

    if query_time < package.delivered_time:
        return PackageStatus.EN_ROUTE

    return PackageStatus.DELIVERED

# Displays one package and its status at a given time.
def display_package(package, query_time):

    status = get_status_at_time(package, query_time)

    address, zip_code = get_address_at_time(package, query_time)

    assigned_truck = "Not assigned"

    if (
        package.departure_time is not None
        and query_time >= package.departure_time
    ):
        assigned_truck = package.assigned_truck


    delivered_time = (
        format_time(package.delivered_time)
        if status == PackageStatus.DELIVERED
        else "N/A"
    )

    print(
        f"Package {package.id} | "
        f"Address: {address} | "
        f"City: {package.city} | "
        f"State: {package.state} | "
        f"Zip: {zip_code} | "
        f"Deadline: {format_deadline(package.deadline)} | "
        f"Weight: {package.weight} | "
        f"Status: {status.value} | "
        f"Assigned Truck: {assigned_truck} | "
        f"Delivered: {delivered_time}"
    )

# Displays every package at a requested time.
def display_all_packages(packages, query_time):
    for package in sorted(packages, key=lambda package: package.id):
        display_package(package,query_time)

# This is to improve time readability, converting
# 'minutes past midnight' to HH:MM AM/PM.
def format_time(minutes):
    if minutes is None:
        return "N/A"

    total_minutes = round(minutes)
    hours = total_minutes // 60
    minutes_remaining = total_minutes % 60
    period = "AM" if hours < 12 else "PM"
    display_hour = hours % 12

    if display_hour == 0:
        display_hour = 12

    return f"{display_hour}:{minutes_remaining:02d} {period}"

def format_deadline(deadline):
    if deadline == 1440:
        return "EOD"

    return format_time(deadline)

def get_address_at_time(package, query_time):

    # If the address was corrected after the requested time,
    # return the original address and ZIP code.
    if (
        package.address_corrected_at is not None
        and query_time < package.address_corrected_at
    ):
        return (
            package.original_address,
            package.original_zip_code
        )

    return package.address, package.zip_code