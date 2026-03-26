from pydantic import BaseModel


class ProductoVenta(BaseModel):
    producto_id:int
    cantidad:int

class VentaCreate(BaseModel):
    items :list[ProductoVenta]