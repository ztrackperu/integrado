from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.concepto_ot import (
    add_concepto_ot,
    delete_concepto_ot,
    retrieve_concepto_ot,
    retrieve_concepto_ots,
    update_concepto_ot,
    extraer_concepto_ot,
    validar_concepto_ot,
    regex_concepto_ot,
    regex_insumo,
    validar_insumo_ot,
    codigo_insumo,
    regex_cotizacion,
)
#Aqui importamos el modelo necesario para la clase 
from server.models.concepto_ot import (
    ErrorResponseModel,
    ResponseModel,
    ConceptoOTSchema,
    UpdateConceptoOTModel,
    ConceptoOTSchemaValidar,
)
#aqui se definen las rutas de la API REST
router = APIRouter()


@router.post("/", response_description="Datos de los concepto_ot agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_concepto_ot_data(concepto_ot: ConceptoOTSchema = Body(...)):
    #convertir en json
    concepto_ot = jsonable_encoder(concepto_ot)   
    #print(concepto_ot)
    #enviar a la funcion añadir  
    new_concepto_ot = await add_concepto_ot(concepto_ot)
    return ResponseModel(new_concepto_ot, "ok")

@router.get("/", response_description="Concepto_ot recuperados")
async def get_concepto_ots():
    concepto_ots = await retrieve_concepto_ots()
    if concepto_ots:
        return ResponseModel(concepto_ots, "Datos de los conceptosOT recuperados exitosamente.")
    return ResponseModel(concepto_ots, "Lista vacía devuelta")


@router.get("/{id}", response_description="Datos de conceptoOT recuperados")
async def get_concepto_ot_data(id: int):
    concepto_ot = await retrieve_concepto_ot(id)
    if concepto_ot:
        return ResponseModel(concepto_ot, "Datos del ConceptoOT recuperado exitosamente")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")


@router.put("/{id}")
async def update_concepto_ot_data(id: int, req: UpdateConceptoOTModel = Body(...)):
    #ANALIZADOR DE ESTRUCTURA req
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_concepto_ot = await update_concepto_ot(id, req)
    if updated_concepto_ot:
        return ResponseModel(
            #"ConceptoOT with ID: {} name update is successful".format(id),
            "ok",
            "ConceptoOT name updated successfully",
        )
    return ErrorResponseModel("An error occurred",404,"There was an error updating the ConceptoOT data.",)

@router.delete("/{id}", response_description="concepto_ot data deleted from the database")
async def delete_concepto_ot_data(id: int):
    deleted_concepto_ot = await delete_concepto_ot(id)
    if deleted_concepto_ot:
        return ResponseModel(
            "concepto_ot with ID: {} removed".format(id), "concepto_ot deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "concepto_ot with id {0} doesn't exist".format(id)
    )

@router.get("/maximo/", response_description="El conceptoOT maximo")
async def get_maximo_concepto_ot_data():
    concepto_ot = await extraer_concepto_ot()
    if concepto_ot:
        return ResponseModel(concepto_ot, "Datos del ConceptoOT maximo recuperado ")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")


@router.post("/validar/", response_description="Validar descripcion de  concepto_ot en la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_concepto_ot_data_validar(concepto_ot: ConceptoOTSchemaValidar = Body(...)):
    concepto_ot = jsonable_encoder(concepto_ot)   
    val_concepto_ot = await validar_concepto_ot(concepto_ot)
    return ResponseModel(val_concepto_ot, "El concepto_ot agregó exitosamente.")

@router.get("/regex/{id}", response_description="Datos de conceptoOT con regex ")
async def get_concepto_ot_regex(id: str):
    concepto_ot = await regex_concepto_ot(id)
    if concepto_ot:
        return ResponseModel(concepto_ot, "Datos del ConceptoOT recuperado en regex")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

@router.get("/buscarInsumo/{id}", response_description="Datos de insumos con regex ")
async def get_concepto_ot_regex(id: str):
    concepto_ot = await regex_insumo(id)
    if concepto_ot:
        return ResponseModel(concepto_ot, "Datos de los insumos recuperado en regex")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

@router.post("/validarInsumo/", response_description="Validar descripcion de  concepto_ot en la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_insumo_data_validar(concepto_ot: dict = Body(...)):
    concepto_ot = jsonable_encoder(concepto_ot)   
    val_concepto_ot = await validar_insumo_ot(concepto_ot)
    return ResponseModel(val_concepto_ot, "Los insumo han sido validados ")


@router.get("/infoInsumo/{id}", response_description="Datos de insumos con regex ")
async def get_infoInsumo(id: str):
    concepto_ot = await codigo_insumo(id)
    if concepto_ot:
        return ResponseModel(concepto_ot, "Datos de los insumos recuperado en regex")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

@router.get("/buscarCotizacion/{id}", response_description="Datos de insumos con regex ")
async def get_cotizacion_regex(id: str):
    concepto_ot = await regex_cotizacion(id)
    if concepto_ot:
        return ResponseModel(concepto_ot, "Datos de las cotizaciones recuperado en regex")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")