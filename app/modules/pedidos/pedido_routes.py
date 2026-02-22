from .schemas import PedidoItemCreate, ResponsePedido, DetalleItem,PedidoMesa, DetalleOut
from fastapi import Depends,APIRouter,HTTPException
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.modules.pedidos import crud


router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.get("/",response_model=list[ResponsePedido])
def listar_pedidos(db:Session = Depends(get_db)):
    return crud.get_pedidos(db)

@router.get("/{pedido_id}/info", response_model=ResponsePedido)
def obtener_pedido(pedido_id:int,db:Session = Depends(get_db)):
    
    pedido = crud.get_pedido(db,pedido_id)
    if not pedido:
        raise HTTPException(status_code=400, detail="Plato no encontrado")
    return pedido

@router.get("/{pedido_id}",response_model=list[DetalleItem])
def obtenerDetalles(pedido_id:int,db:Session = Depends(get_db)):
    return crud.get_detalle(db,pedido_id)

@router.get("/mesa/{mesa_id}", response_model=list[DetalleOut])
def obtenerPedidoMesa(mesa_id:int,db:Session = Depends(get_db)):
    return crud.get_pedido_activo_mesa(db,mesa_id)

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