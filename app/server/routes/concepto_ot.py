from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


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
    regex_proveedores,
    ListaUnidadMedidaF,
    ListaSolicitanteOTF,
    ListaSupervisadoOTF,
    ListaFormaPagoMF,
    ListaPlazoMF,
    ListaTecnicoOTF,
    concepto_filtrado_periodo,
    buscarProductoOTF,
    codigo_dispositivo,
    regex_codigoAlquilerVenta,
    regex_codigoDisponible,
    regex_buscarCodigo,
    retrieve_stock_validar,
    validar_insumo_ot2,
    validar_insumo_ot3,
    ultimaOt,
    ultimaSolicitud,
    guardar_solicitud,
    BuscarSolicitud,
    guardar_otGeneral,
    BuscarOTGeneral,
    MostrarOT,
)
#Aqui importamos el modelo necesario para la clase 
from server.models.concepto_ot import (
    ErrorResponseModel,
    ResponseModel,
    ConceptoOTSchema,
    UpdateConceptoOTModel,
    ConceptoOTSchemaValidar,
    SolicitudSchema,
    OTSchema,
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

@router.get("/buscarProveedor/{id}", response_description="Datos de insumos con regex ")
async def get_proveedor_regex(id: str):
    concepto_ot = await regex_proveedores(id)
    if concepto_ot:
        return ResponseModel(concepto_ot, "Datos de las cotizaciones recuperado en regex")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")


#viene de la otra api

@router.get("/ListaUnidadMedida/")
async def ListaUnidadMedida():
    item_details = await ListaUnidadMedidaF()
    if item_details:
        return JSONResponse(item_details)
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

@router.get("/ListaSolicitanteOT/")
async def ListaSolicitanteOT():
    item_details = await ListaSolicitanteOTF()
    if item_details:
        return JSONResponse(item_details)
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

@router.get("/ListaSupervisadoOT/")
async def ListaSupervisadoOT():
    item_details = await ListaSupervisadoOTF()
    if item_details:
        return JSONResponse(item_details)
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

@router.get("/ListaFormaPagoM/")
async def ListaFormaPagoM():
    item_details = await ListaFormaPagoMF()
    if item_details:
        return JSONResponse(item_details)
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

@router.get("/ListaPlazoM/")
async def ListaPlazoM():
    item_details = await ListaPlazoMF()
    if item_details:
        return JSONResponse(item_details)
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

@router.get("/ListaTecnicoOT/")
async def ListaTecnicoOT():
    item_details = await ListaTecnicoOTF()
    if item_details:
        return JSONResponse(item_details)
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

@router.post("/ConceptoPeriodo/")
async def ConceptoPeriodoF(concepto_ot: dict = Body(...)):
    concepto_ot = jsonable_encoder(concepto_ot)   
    val_concepto_ot = await concepto_filtrado_periodo(concepto_ot)
    return JSONResponse(val_concepto_ot)
    #return ResponseModel(val_concepto_ot, "Los insumo han sido validados ")

@router.get("/buscarProductoOT/{id}", response_description="Datos de insumos con regex ")
async def buscarProductoOT(id: str):
    concepto_ot = await buscarProductoOTF(id)
    if concepto_ot:
        return ResponseModel(concepto_ot, "Datos de las cotizaciones recuperado en regex")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

@router.get("/buscarCodigo/{id}", response_description="Datos de insumos con regex ")
async def codigo_dispositivoF(id:str):
    item_details = await codigo_dispositivo(id)
    if item_details:
        return JSONResponse(item_details)
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

@router.get("/buscarCodigoAlquilerVenta/{id}", response_description="Datos de insumos con regex ")
async def regex_codigoAlquilerVentaF(id: str):
    concepto_ot = await regex_codigoAlquilerVenta(id)
    if concepto_ot:
        return ResponseModel(concepto_ot, "Datos de CodigoAlquilerVenta recuperado en regex")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

@router.get("/buscarCodigoDisponible/{id}", response_description="Datos de insumos con regex ")
async def regex_codigoDisponibleF(id: str):
    concepto_ot = await regex_codigoDisponible(id)
    if concepto_ot:
        return ResponseModel(concepto_ot, "Datos de CodigoDisponible recuperado en regex")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

@router.get("/ExtraerCodigo/{id}", response_description="Datos de insumos con regex ")
async def regex_buscarCodigoF(id:str):
    item_details = await regex_buscarCodigo(id)
    if item_details:
        return JSONResponse(item_details)
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

#aqui va la los datos recuperados con stock 

@router.get("/StockValidado/{id}", response_description="Datos con stock  recuperados")
async def get_concepto_ot_data(id: int):
    concepto_ot = await retrieve_stock_validar(id)
    
    if concepto_ot:
        return ResponseModel(concepto_ot, "Datos de la plantilla con  Stock  recuperado exitosamente")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")


@router.post("/validarInsumoOT/", response_description="Validar descripcion de  concepto_ot en la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_insumo_data_validar_OT(concepto_ot: dict = Body(...)):
    concepto_ot = jsonable_encoder(concepto_ot)   
    #val_concepto_ot = await validar_insumo_ot2(concepto_ot)
    val_concepto_ot = await validar_insumo_ot3(concepto_ot)
    return ResponseModel(val_concepto_ot, "Los insumo OT han sido validados ")

@router.get("/UltimaOT/")
async def ultimaOtF():
    item_details = await ultimaOt()
    if item_details:
        return JSONResponse(item_details)
    return ErrorResponseModel("Ocurrió un error.", 404, "problemas al obtener el ultimo ot")

@router.get("/UltimaSolicitud/")
async def ultimaSolicitudF():
    item_details = await ultimaSolicitud()
    if item_details:
        return JSONResponse(item_details)
    return ErrorResponseModel("Ocurrió un error.", 404, "problemas al obtener LA ULTIMA SOLICITUD")

#GuardarSolicitud
@router.post("/GuardarSolicitud/", response_description="Guardar solicitud en la base de datos.")
async def add_solicitud(concepto_ot: SolicitudSchema = Body(...)):
    #convertir en json
    concepto_ot = jsonable_encoder(concepto_ot)   
    #print(concepto_ot)
    #enviar a la funcion añadir  
    new_concepto_ot = await guardar_solicitud(concepto_ot)
    return ResponseModel(new_concepto_ot, "La solicitud ha sido guardado ")

#BuscarSolicitud
@router.get("/BuscarSolicitud/{id}", response_description="Datos de solicitud") 
async def BuscarSolicitud_data(id: int):
    concepto_ot = await BuscarSolicitud(id)
    if concepto_ot:
        return ResponseModel(concepto_ot, "Datos de la solicitud recuperado exitosamente")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

#GuardarSolicitud
@router.post("/GuardarOTGeneral/", response_description="Guardar OT en la base de datos.")
async def add_otGeneral(concepto_ot: OTSchema = Body(...)):
    #convertir en json
    concepto_ot = jsonable_encoder(concepto_ot)   
    #print(concepto_ot)
    #enviar a la funcion añadir  
    new_concepto_ot = await guardar_otGeneral(concepto_ot)
    return ResponseModel(new_concepto_ot, "La solicitud ha sido guardado ")

#BuscarOTGeneral
@router.get("/BuscarOTGeneral/{id}", response_description="Datos de solicitud") 
async def BuscarOTGeneral_data(id: int):
    concepto_ot = await BuscarOTGeneral(id)
    if concepto_ot:
        return ResponseModel(concepto_ot, "Datos de la OT recuperado exitosamente")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

#BuscarOTGeneral
@router.get("/MostrarOT/{id}", response_description="Datos de solicitud") 
async def MostrarOT_data(id: int):
    concepto_ot = await MostrarOT(id)
    if concepto_ot:
        return ResponseModel(concepto_ot, "Datos de la OT recuperado exitosamente")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")