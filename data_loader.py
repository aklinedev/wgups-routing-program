# This module will be responsible for parsing the data into the
# correct objects from the given data. This way, it can be reused with
# more data, rather then hard coding the values, allowing for scalability.

# Using load_workbook from openpyxl to parse data.
from openpyxl import load_workbook
from package import Package
from hash_table import HashTable
from datetime import datetime

# Loads the package data into a custom hash table, deals with special
# notes explicitly with a helper.
def load_packages(file_path):
    workbook = load_workbook(file_path)
    sheet = workbook["Sheet1"]
    rows = list(sheet.iter_rows(
    min_row=9,
    max_row=48,
    min_col=1,
    max_col=8,
    values_only=True
))
    packages = HashTable(len(rows))

    for row in rows:
        package_id, address, city, state, zip_code, deadline, weight, special_note = row

        package = Package(
            package_id,
            address,
            city,
            state,
            str(zip_code),
            deadline,
            weight,
            special_note
    )
        
        _parse_special_notes(package)
        packages.insert(package.id, package)

    return packages
        
    
def _parse_special_notes(package):
    if not package.special_note:
        return
    # Can only be on X truck, detected by the string "Can only be on truck",
    # and must have the truck number as the last word in the string.
    elif "Can only be on truck" in package.special_note:
        parts = package.special_note.split()
        truck_number = int(parts[-1])
        package.required_truck = truck_number

    # Package delayed is detected by the string "Delayed" some where in the note
    # and it must end with "until hh:mm am/pm" to be valid.
    elif "Delayed" in package.special_note:
        time_string = package.special_note.split("until ")[1]
        package.available_at = _time_to_minutes(time_string)

    # Must be delivered with x,y, detected by the string "Must be delivered with".
    # Extracts the package IDs listed after "with", separated by commas
    elif "Must be delivered with" in package.special_note:
        delivered_with = package.special_note.split("with ")[1]
        ids = delivered_with.split(",")
        grouped_ids = [int(package_id.strip()) for package_id in ids]
        package.grouped_with = grouped_ids

    elif "Wrong address" in package.special_note:
        package.address_is_valid = False


# Use this helper to convert any given time 12 hour in the format of HH:MM am/pm.
def _time_to_minutes(time_string):
    parsed_time = datetime.strptime(time_string.strip(), "%I:%M %p")
    return parsed_time.hour * 60 + parsed_time.minute

