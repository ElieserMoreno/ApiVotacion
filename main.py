from fastapi import FastAPI
from database import engine, Base
from routers import voters, candidates, votes


# Importa los modelos para asegurarte de que se registren
import models

app = FastAPI()

# Crear las tablas en la base de datos
app.include_router(voters.router)
app.include_router(candidates.router)
app.include_router(votes.router)


Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "¡API de Votación lista!"}
