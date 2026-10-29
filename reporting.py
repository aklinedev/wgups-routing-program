from package import PackageStatus

# This is the "Supervisor Function". This module
# is imported to main, and I have made two lookup
# calls at the bottom of main, they are commented out.

# Returns what the package's status would have been
# at the requested point in simulated time.
def get_status_at_time(package, query_time):

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

    print(
        f"Package {package.id} | "
        f"Address: {package.address} | "
        f"City: {package.city} | "
        f"State: {package.state} | "
        f"Zip: {package.zip_code} | "
        f"Deadline: {format_time(package.deadline)} | "
        f"Weight: {package.weight} | "
        f"Status: {status.value} | "
        f"Delivered: {format_time(package.delivered_time)}"
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