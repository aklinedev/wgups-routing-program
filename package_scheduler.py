from package import PackageStatus

def build_load(packages, truck, current_time):

    load = []
    sorted_packages = _sort_packages(packages, truck)

    for package in sorted_packages:
        remaining_capacity = truck.capacity - len(load)

        # Check if load size is at capcity for given truck
        if len(load) >= truck.capacity:
            break

        # Since we have grouped packages, check if it has already been loaded.
        if package in load:
            continue

        # Checking basic eligiblity of packages
        if not _is_eligible_package(package, truck, current_time):
            continue

        # This if block handles grouped packages by calling helpers to
        # check eligiblity and ensure they wont exceed the remaining capacity.
        if package.grouped_with is not None:
            group = _handle_grouped_packages(package, packages)
            if group is None:
                continue
            if not _can_grouped_packages_fit(group, remaining_capacity):
                continue
            if not all(_is_eligible_package(p, truck, current_time) for p in group):
                continue
            for grouped_package in group:
                if grouped_package not in load:
                    load.append(grouped_package)
            continue


        load.append(package)

    return load


def _is_eligible_package(package, truck, current_time):
    if package.status is not PackageStatus.AT_HUB:
        return False
    
    if package.available_at is not None:
        if package.available_at > current_time:
                return False
        
    if not package.address_is_valid:
        return False
    
    if package.required_truck is not None:
        if package.required_truck != truck.id:
            return False

    return True


def _handle_grouped_packages(package, packages):
    group = [package]
    for grouped_id in package.grouped_with:
        grouped_package = packages.get(grouped_id)
        if grouped_package is None:
            return None
        group.append(grouped_package)

    return group

    
def _can_grouped_packages_fit(group, remaining_capacity):
    return len(group) <= remaining_capacity


def _sort_packages(packages, truck):
    return sorted(
        packages, key=lambda package: 
        (package.deadline, 0 if package.required_truck == truck.id else 1)
    )

