from fastapi import FastAPI

from server.routes.student import router as StudentRouter

app = FastAPI(
    title="Integracion Intranet",
    summary="Modulos de datos bidireccional",
    version="0.0.1",

)

#añadir el conjunto de archivos a StudentRouter con la url "student"
app.include_router(StudentRouter, tags=["Student"], prefix="/student")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
