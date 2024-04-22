from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.student import (
    add_student,
    delete_student,
    retrieve_student,
    retrieve_students,
    update_student,
)
#Aqui importamos el modelo necesario para la clase 
from server.models.student import (
    ErrorResponseModel,
    ResponseModel,
    StudentSchema,
    UpdateStudentModel,
)
#aqui se definen las rutas de la API REST
router = APIRouter()


@router.post("/", response_description="Datos de los estudiantes agregados a la base de datos.")
#La funcion espera "StudentSchema"
async def add_student_data(student: StudentSchema = Body(...)):
    #convertir en json
    student = jsonable_encoder(student)
    
    print(student)

    #enviar a la funcion añadir  
    new_student = await add_student(student)
    return ResponseModel(new_student, "El estudiante agregó exitosamente.")


@router.get("/", response_description="Students retrieved")
async def get_students():
    students = await retrieve_students()
    if students:
        return ResponseModel(students, "Students data retrieved successfully")
    return ResponseModel(students, "Empty list returned")


@router.get("/{id}", response_description="Student data retrieved")
async def get_student_data(id):
    student = await retrieve_student(id)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")


@router.put("/{id}")
async def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_student = await update_student(id, req)
    if updated_student:
        return ResponseModel(
            "Student with ID: {} name update is successful".format(id),
            "Student name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="Student data deleted from the database")
async def delete_student_data(id: str):
    deleted_student = await delete_student(id)
    if deleted_student:
        return ResponseModel(
            "Student with ID: {} removed".format(id), "Student deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Student with id {0} doesn't exist".format(id)
    )
