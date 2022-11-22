from enum import Enum


class StatusEnum(str, Enum):
    Active = "Active"
    Inactive = "Inactive"
    Unknown = "Unknown"
