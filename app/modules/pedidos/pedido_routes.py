from app.modules.auth.auth import get_current_user
from app.models.user import User
from .schemas import PedidoItemCreate, ResponsePedido, DetalleItem,PedidoMesa, DetalleOut
from fastapi import Depends,APIRouter,HTTPException
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.modules.pedidos import crud
from pydantic import BaseModel


router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


class ActualizarEstadoPedido(BaseModel):
    estado: str


@router.get("/",response_model=list[ResponsePedido])
def listar_pedidos(db:Session = Depends(get_db)):
    return crud.get_pedidos(db)

@router.get("/mesa/{mesa_id}", response_model=list[DetalleOut])
def obtenerPedidoMesa(mesa_id:int,db:Session = Depends(get_db)):
    return crud.get_pedido_activo_mesa(db,mesa_id)

@router.get("/{pedido_id}/info", response_model=ResponsePedido)
def obtener_pedido(pedido_id:int,db:Session = Depends(get_db)):
    
    pedido = crud.get_pedido(db,pedido_id)
    if not pedido:
        raise HTTPException(status_code=400, detail="Plato no encontrado")
    return pedido

@router.get("/{pedido_id}",response_model=list[DetalleItem])
def obtenerDetalles(pedido_id:int,db:Session = Depends(get_db)):
    return crud.get_detalle(db,pedido_id)

@router.patch("/{pedido_id}/estado", response_model=ResponsePedido)
def actualizar_estado(pedido_id:int, data: ActualizarEstadoPedido, db:Session = Depends(get_db)):
    """Actualizar el estado de un pedido"""
    return crud.actualizar_estado_pedido(db, pedido_id, data.estado)

@router.post("/", status_code=201)
def create(pedido: PedidoItemCreate,db:Session = Depends(get_db)):
    return crud.crear_pedido(
        db=db,
        usuario_id=pedido.user_id,
        pedido_data=pedido
    )

@router.post("/create",status_code=201)
def crearPedidoMesa(pedido: PedidoMesa, db:Session = Depends(get_db)):
    return crud.crear_pedido_mesa(
        db=db,
        usuario_id=pedido.user_id,
        mesa_id=pedido.mesa_id,
        pedido_data=pedido
    )
@router.post("/mesa/", response_model=ResponsePedido)
def agregar_platillo_mesa(pedido:PedidoMesa,current_user: User =Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.agregar_plato(
        db=db,
        mesa_id = pedido.mesa_id,
        negocio_id=current_user.empleado.negocio_id,
        item=pedido.items[0] if pedido.items else None
    )