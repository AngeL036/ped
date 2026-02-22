from sqlalchemy.orm import Session, joinedload
from app.models.pedido import Pedido
from app.models.empleado import Empleado
from app.models.user import User
from app.modules.pedidos.schemas import PedidoItemCreate
from app.models.plato import Plato
from app.models.detallePedido import DetallePedido
from fastapi import HTTPException

def get_pedidos(db:Session):
    return db.query(Pedido).all()

def get_pedido(db:Session, pedido_id:int):
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()

def get_detalle(db:Session, pedido_id:int):
    print(f"pedido_id: {pedido_id}")
    return db.query(DetallePedido).filter(DetallePedido.pedido_id == pedido_id).all()

def get_pedido_mesa(db:Session,mesa_id):
    return  db.query(Plato).filter_by(mesa_id).all()

def get_pedido_activo_mesa(db:Session, mesa_id:int):
    pedido = (
        db.query(Pedido)
        .options(joinedload(Pedido.detalles).joinedload(DetallePedido.platillo))
        .filter(
            Pedido.mesa_id == mesa_id,
            Pedido.estado == "abierto"
        )
        .first()
    )
    if not pedido:
        return []
    return pedido.detalles


def get_or_create_pedido_activo(db:Session, mesa_id:int,negocio_id:int):
    pedido = (
        db.query(Pedido)
        .filter(
            Pedido.mesa_id == mesa_id,
            Pedido.estado == "abierto"
        )
        .first()
    )
    if pedido:
        return pedido
    pedido = Pedido(
            mesa_id=mesa_id,
            negocio_id=negocio_id,
            estado="abierto",
            total=0
        )
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    
    return pedido
def agregar_plato(db:Session,mesa_id:int,negocio_id:int,item):
    pedido = get_or_create_pedido_activo(db,mesa_id,negocio_id)

    plato = db.query(Plato).get(item.platillo_id)
    subtotal = plato.precio * item.cantidad

    detalle = DetallePedido(
        pedido_id=pedido.id,
        platillo_id=plato.id,
        cantidad=item.cantidad,
        precio_unitario=plato.precio,
        subtotal=subtotal
    )
    pedido.total += subtotal

    db.add(detalle)
    db.commit()
    
    return pedido

def cerrar_pedido(db: Session, mesa_id: int):

    pedido = (
        db.query(Pedido)
        .filter(
            Pedido.mesa_id == mesa_id,
            Pedido.estado == "abierto"
        )
        .first()
    )

    if not pedido:
        raise HTTPException(404, "No hay pedido abierto")

    pedido.estado = "cerrado"

    db.commit()

    return pedido


def actualizar_estado_pedido(db: Session, pedido_id: int, nuevo_estado: str):
    """Actualizar el estado de un pedido"""
    estados_validos = ["abierto", "pendiente", "en_preparacion", "listo", "servido", "cerrado", "cancelado"]
    
    if nuevo_estado not in estados_validos:
        raise HTTPException(
            status_code=400,
            detail=f"Estado inválido. Estados permitidos: {', '.join(estados_validos)}"
        )
    
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    pedido.estado = nuevo_estado
    db.commit()
    db.refresh(pedido)
    return pedido


def crear_pedido_mesa(db:Session,usuario_id:int,mesa_id:int,pedido_data:PedidoItemCreate):
    try:
        user = db.query(User).filter(User.id == usuario_id).first()
        if not user:
            raise HTTPException(
        status_code=400,
        detail="El usuario no existe"
        )
        empleado = db.query(Empleado).filter(Empleado.user_id == user.id).first()
        if not empleado:
                raise HTTPException(400, "El usuario no es empleado")
        total = 0
        pedido = Pedido(
            negocio_id=empleado.negocio_id,
            mesa_id=mesa_id,
            mesero_id=empleado.id,
            total = 0,
            
        )
        db.add(pedido)
        db.flush()

        for item in pedido_data.items:
            platillo = db.query(Plato).filter(Plato.id == item.platillo_id).first()
            if not platillo:
                raise HTTPException(
                    status_code=404,
                    detail=f"Platillo {item.platillo_id} no existe"
                )
            
            precio = platillo.precio * item.cantidad
            total = total + precio
            subtotal = item.cantidad * platillo.precio
            precio_unitario = platillo.precio
            detalle = DetallePedido(
                pedido_id = pedido.id,
                platillo_id = item.platillo_id,
                precio_unitario = precio_unitario,
                cantidad=item.cantidad,
                subtotal=subtotal
            )
            db.add(detalle)
        pedido.total = total
        db.commit()
        db.refresh(pedido)

        return{
            "message":"Pedido confirmado",
            "pedido_id":pedido.id,
            "total":pedido.total
        }   
    except Exception as e:
        db.rollback()
        print(" ERROR:", e)
        raise

        
def crear_pedido(db:Session,usuario_id:int,pedido_data:PedidoItemCreate):
    try:
        user = db.query(User).filter(User.id == usuario_id).first()
        if not user:
            raise HTTPException(
        status_code=400,
        detail="El usuario no existe"
        )
        total = 0
        pedido = Pedido(
            usuario_id=usuario_id,
            direccion_envio = "direccion prueba",
            total = 0,
        )
        db.add(pedido)
        db.flush()

        for item in pedido_data.items:
            platillo = db.query(Plato).filter(Plato.id == item.platillo_id).first()
            if not platillo:
                raise HTTPException(
                    status_code=404,
                    detail=f"Platillo {item.platillo_id} no existe"
                )
            
            precio = platillo.precio * item.cantidad
            total = total + precio
            subtotal = item.cantidad * platillo.precio
            precio_unitario = platillo.precio
            detalle = DetallePedido(
                pedido_id = pedido.id,
                platillo_id = item.platillo_id,
                precio_unitario = precio_unitario,
                cantidad=item.cantidad,
                subtotal=subtotal
            )
            db.add(detalle)
        pedido.total = total
        db.commit()
        db.refresh(pedido)

        return{
            "message":"Pedido confirmado",
            "pedido_id":pedido.id,
            "total":pedido.total
            }   
    except Exception as e:
        db.rollback()
        print(" ERROR:", e)
        raise



