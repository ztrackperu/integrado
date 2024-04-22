from typing import Optional,List

from pydantic import BaseModel, EmailStr, Field

#clase necesaria para establecer el esquema de datos para la clase Student
class StudentSchema(BaseModel):
    #Field(...) hace referencia a que el campo es obligatorio
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    course_of_study: str = Field(...)
    year: int = Field(..., gt=0, lt=9)
    #gpa: float = Field(..., le=4.0)
    gpa: Optional[float] | None =None
    rela: Optional[List] | None =None


    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources engineering",
                "year": 2,
                "gpa": "3.0",
                "rela" :
                    [
                        {"name":"Luis"},
                        {"name": "Pablo"},
                    ]
                
            }
        }


class UpdateStudentModel(BaseModel):
    fullname: Optional[str]| None =None
    email: Optional[EmailStr]| None =None
    course_of_study: Optional[str]| None =None
    year: Optional[int]| None =None
    gpa: Optional[float]| None =None
    rela: Optional[List] | None =None

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources and environmental engineering",
                "year": 4,
                "gpa": "4.0",
                "rela" :
                    [
                        {"name":"Luis"},
                        {"name": "Pablo"},
                    ]
            }
        }

#respuesta cuando todo esta bien
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


#respuesta cuando algo sale mal 
def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
