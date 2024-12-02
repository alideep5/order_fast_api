from dataclasses import dataclass


@dataclass
class Product:
    id: str
    shop_id: str
    name: str
    price: float
