from dataclasses import dataclass


@dataclass
class Shop:
    id: str
    name: str
    address: str
    owner_id: str
