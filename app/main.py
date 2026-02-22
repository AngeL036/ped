from app.models import *
from fastapi.middleware.cors import CORSMiddleware


from app.modules.pedidos.pedido_routes import router as pedidos_router
from app.modules.platos.routes import router as platos_router
from app.modules.auth.user_routes import router_user
from app.modules.mesas.routes import router as router_mesas
from app.modules.pago.router import router as pagos_router
from app.modules.empleado.routes import router as empleado_router
from app.modules.negocio.routes import router as negocio_router
from fastapi import FastAPI
from app.database import engine, Base

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],  # Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(pedidos_router)
app.include_router(platos_router)
app.include_router(router_user)
app.include_router(router_mesas)
app.include_router(pagos_router)
app.include_router(empleado_router)
app.include_router(negocio_router)




@app.get("/")
def root():
    return {"status":"Api funcionando"}