from server.database import collection



student_collection = collection("students_collection")

# helpers

#esta es la estructura esperda que se imprime como resultado
def student_helper(student) -> dict: 
    #print(student["rela"])
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
        #"rela": validar_lista(student["rela"]),
        "rela":  student.get("rela",None),
        #"rela": "oli",
    }


# crud operations


# Retrieve all students present in the database
async def retrieve_students():
    students = []
    async for student in student_collection.find():
        print(student)
        students.append(student_helper(student))
    return students


# Agregar un nuevo estudiante a la base de datos
async def add_student(student_data: dict) -> dict:
    #aqui envia el json a mongo y lo inserta
    student = await student_collection.insert_one(student_data)
    #aqui busca el dato obtenido para mostrarlo como respuesta
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


# Retrieve a student with a matching ID
async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student) 


# Update a student with a matching ID
async def update_student(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_student:
            return True
        return False

# Delete a student from the database
async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True
