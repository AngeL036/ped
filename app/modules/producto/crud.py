from app.models.producto import Producto
from app.modules.inventario.schemas import ProductoInicialCreate
from sqlalchemy.orm import Session
from app.models.inventarios import Inventario
from app.models.movimientoInventario import MovimientoInventario, TipoMovimiento, MotivoMovimiento


def _estado_stock(cantidad:int,minimo:int) -> str:
    if cantidad <= 0:
        return "REPONER"
    if cantidad <= minimo:
        return "BAJO"
    return "OK"

def _build_response(producto:Producto) -> dict:
    """Construye el ProductoResponse enriquecido con precios y estados."""
    ultimo = (
        producto.inventario[-1] if producto.inventario else None
    )
    return {
        **producto.__dict__,
        "precio_compra": float(producto.precio_compra) if producto.precio_compra else None,
        "precio_venta": float(producto.precio_venta) if producto.precio_venta else None,
        "estado_stock": _estado_stock(producto.cantidad_actual, producto.stock_minimo),
    }

def create_product(db:Session, product:ProductoInicialCreate, negocio_id:int):
    """ crear un producto"""
    nuevo_producto = Producto(
        negocio_id = negocio_id,
        categoria_id = product.producto.categoria_id,
        codigo = product.producto.codigo,
        nombre = product.producto.nombre,
        unidad = product.producto.unidad,
        cantidad_actual = product.inventario.cantidad,
        stock_minimo = product.producto.stock_minimo,
        precio_compra = product.precios.precio_compra,
        precio_venta = product.precios.precio_venta,
        activo = True,

    )
    db.add(nuevo_producto)
    db.flush()

    conteo = Inventario(
        producto_id = nuevo_producto.id,
        cantidad    = product.inventario.cantidad,
        motivo      = product.inventario.motivo or " conteo inicial",
    )
    db.add(conteo)

    movimiento = MovimientoInventario(
        producto_id = nuevo_producto.id,
        tipo = TipoMovimiento.entrada,
        cantidad = product.inventario.cantidad,
        motivo = MotivoMovimiento.conteo_fisico,
    )
    db.add(movimiento)
    db.commit()
    db.refresh(nuevo_producto)

    return {"producto": _build_response(nuevo_producto), "inventario": conteo}

def list_product(db:Session, negocio_id:int):
    productos = db.query(Producto).filter(Producto.negocio_id == negocio_id, Producto.activo == True).all()
    return [_build_response(p) for p in productos]