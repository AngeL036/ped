from app.models import *
from fastapi.middleware.cors import CORSMiddleware


from app.modules.pedidos.pedido_routes import router as pedidos_router
from app.modules.platos.routes import router as platos_router
from app.modules.auth.user_routes import router_user
from app.modules.mesas.routes import router as router_mesas
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




@app.get("/")
def root():
    return {"status":"Api funcionando"}