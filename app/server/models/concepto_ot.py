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