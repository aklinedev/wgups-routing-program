from enum import Enum

# Defining what a package status represents
class PackageStatus(Enum):
    AT_HUB = "AT_HUB"
    EN_ROUTE = "EN_ROUTE"
    DELIVERED = "DELIVERED"

# Package is used to define a package object and its data.
# Constructors assigned with none are not required to create a 
# package object.

class Package:
    def __init__(
        self,
        id,
        address,
        city,
        state,
        zip_code,
        deadline,
        weight,
        special_note,
        status = PackageStatus.AT_HUB,
        grouped_with=None,
        required_truck=None,
        available_at=None,
        address_is_valid=True,
        assigned_truck=None,
        departure_time=None,
        delivered_time=None
    ):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_note = special_note
        self.status = status

        self.grouped_with = grouped_with
        self.required_truck = required_truck
        self.available_at = available_at
        self.address_is_valid = address_is_valid
        

        self.assigned_truck = assigned_truck
        self.departure_time = departure_time
        self.delivered_time = delivered_time

    def mark_en_route(self, time):
        self.status = PackageStatus.EN_ROUTE
        self.departure_time = time

    def mark_delivered(self, time):
        self.status = PackageStatus.DELIVERED
        self.delivered_time = time
        