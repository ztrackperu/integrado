from typing import Optional,List

from pydantic import BaseModel, Field

#clase necesaria para establecer el esquema de datos para la clase Student
class ConceptoOTSchema(BaseModel):
    #Field(...) hace referencia a que el campo es obligatorio
    id: int = Field(...)
    codigo: int = Field(...)
    descripcion: str = Field(...)
    estado: int = Field(...)
    insumos: Optional[List] | None =None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 105,
                "codigo": 1105,
                "descripcion": "MANTENIMIENTO MAQUINA REEFER",
                "estado": 2,
                "insumos" :
                    [
                        {
                            "codigo_insumo":"RND2020",
                            "nombre_insumo":"Casco Blanco",
                            "medida":"UND",
                            "cantidad":2
                        },
                        {
                            "codigo_insumo":"RND3133",
                            "nombre_insumo":"Tornillo 230",
                            "medida":"UND",
                            "cantidad":13
                        },
                    ]               
            }
        }

class UpdateConceptoOTModel(BaseModel):
    id: Optional[int]| None =None
    codigo: Optional[int]| None =None
    descripcion: Optional[str] | None =None
    estado: Optional[int] | None =None
    insumos: Optional[List] | None =None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 105,
                "codigo": 1105,
                "descripcion": "MANTENIMIENTO MAQUINA REEFER",
                "estado": 2,
                "insumos" :
                    [
                        {
                            "codigo_insumo":"RND2020",
                            "nombre_insumo":"Casco Blanco",
                            "medida":"UND",
                            "cantidad":2
                        },
                        {
                            "codigo_insumo":"RND3133",
                            "nombre_insumo":"Tornillo 230",
                            "medida":"UND",
                            "cantidad":13
                        },
                    ]               
            }
        }

class SolicitudSchema(BaseModel):
    #Field(...) hace referencia a que el campo es obligatorio
    c_numot: int = Field(...)
    numSolicitud: int = Field(...)
    estadoS: int = Field(...)
    fechaS: str = Field(...)
    solicitud: Optional[List] | None =None

    class Config:
        json_schema_extra = {
            "example": {
                "c_numot": 105,
                "numSolicitud": 1105,
                "solicitud" :
                    [
                        {
                            "codigo_insumo":"RND2020",
                            "nombre_insumo":"Casco Blanco",
                            "medida":"UND",
                            "cantidad":2
                        },
                        {
                            "codigo_insumo":"RND3133",
                            "nombre_insumo":"Tornillo 230",
                            "medida":"UND",
                            "cantidad":13
                        },
                    ]               
            }
        }


class OTSchema(BaseModel):
    #Field(...) hace referencia a que el campo es obligatorio
    c_numot:int = Field(...)
    c_desequipo:str = Field(...)
    unidad: str = Field(...)
    d_fecdcto: str = Field(...)
    c_codmon:str = Field(...)
    c_treal:str = Field(...)
    c_asunto: str = Field(...)
    c_supervisa:str = Field(...)
    c_solicita:str = Field(...)
    c_lugartab:str = Field(...)
    c_ejecuta: str = Field(...)
    c_cliente: str = Field(...)
    d_fecentrega: str = Field(...)
    c_usrcrea: str = Field(...)
    d_fcrea: str = Field(...)
    c_estado: str = Field(...)
    c_refcot: str = Field(...)
    c_osb: str = Field(...)
    c_numeroReporte:str = Field(...)
    c_serieEquipo: str = Field(...)
    c_tratopag: str = Field(...)
    c_codpgf: str = Field(...)
    h_inicio:str = Field(...)
    nro_guia: str = Field(...)
    nro_ticket:str = Field(...)
    DetalleOT:Optional[List] | None =None

    class Config:
        json_schema_extra = {
            "example": {
                "c_numot":"c_numot",
                "c_desequipo":"c_desequipo",
                "unidad": "unidad",
                "d_fecdcto": "d_fecdcto",
                "c_codmon":"c_codmon",
                "c_treal": "c_treal",
                "c_asunto": "c_asunto",
                "c_supervisa":"c_supervisa",
                "c_solicita":"c_solicita",
                "c_lugartab":"c_lugartab",
                "c_ejecuta": "c_ejecuta",
                "c_cliente": "c_cliente",
                "d_fecentrega": "d_fecentrega",
                "c_usrcrea": "c_usrcrea",
                "d_fcrea": "d_fcrea",
                "c_estado": "c_estado",
                "c_refcot": "c_refcot",
                "c_osb": "c_osb",
                "c_numeroReporte": "c_numeroReporte",
                "c_serieEquipo": "c_serieEquipo",
                "c_tratopag": "c_tratopag",
                "c_codpgf": "c_codpgf",
                "h_inicio": "h_inicio",
                "nro_guia": "nro_guia",
                "nro_ticket":"nro_ticket",
                "DetalleOT":[
                    {
                        "c_numot": "c_numot",
                        "n_id": "n_id",
                        "c_rucprov": "c_rucprov",
                        "c_nomprov": "c_nomprov",
                        "concepto": "concepto",
                        "tdoc": "tdoc",
                        "ndoc": "ndoc",
                        "fdoc": "fdoc",
                        "monto": "monto",
                        "n_cant": "n_cant",
                        "n_igvd": "n_igvd",
                        "n_totd": "n_totd",
                        "montop":"montop",
                        "c_tecnico": "c_tecnico"        
                    }
                ],           
            }
        }





#respuesta cuando todo esta bien
def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


#respuesta cuando algo sale mal 
def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}



class ConceptoOTSchemaValidar(BaseModel):
    #Field(...) hace referencia a que el campo es obligatorio
    descripcion: str = Field(...)
    class Config:
        json_schema_extra = {
            "example": {
                "descripcion": "MANTENIMIENTO MAQUINA REEFER",            
            }
        }


