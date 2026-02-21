from sqlalchemy.orm import Session
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
    pedido = db.query(Pedido).filter(
            Pedido.mesa_id == mesa_id,
            Pedido.estado == "abierto"
        ).first()
    if not pedido:
        raise HTTPException(
        status_code=404,
        detail="No hay pedidos"
        )
    return pedido.detalles
    
    
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
            subtotal = item.cantidad * item.precio
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



