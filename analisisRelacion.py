import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students

student_collection = database.get_collection("students_collection")

#array para definir si encuentra elemento (2 ->actualizar y 1->añadir)
def buscar_coincidencias(lista1, lista2):
    resultados = []
    for persona1 in lista1:
        encontrado = False
        for persona2 in lista2:
            if persona1['codigo'] == persona2['codigo']:
                encontrado = True
                resultados.append(2) #actualizar
                break
        if not encontrado:
            resultados.append(1) #añadir
    return resultados

#evaluar existencia de lista 
def validar_lista(not_defined):
    try:
        not_defined
    except NameError:
        print("La variable no esta definida")
        return None
    else:
        print("El conteido es:", not_defined)
        return not_defined

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
    #print(data)
    if len(data) < 1:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        print(data)
        #print(student['rela'])
        terrible = data.get("rela",None)
        #print(terrible)
        if terrible :
            data_rela =student.get("rela",None)
            if data_rela :
                print("ya existen valores en la data ")
                #recorres los valores para bsucar insertar actualizar los datos , sino insertar en el array
                #print(len(terrible))
                #primero insertar todo menos el "rela"
                #viene analizis grande 
                #primer comparar los existen con lo que se va insertar
                #si el elemento no esta no esta en los insertados ->eliminar primero
                conjunto = student['rela']
                #evaluar los resultados 
                print(conjunto)
                for persona1 in terrible:
                    encontrado = False
                    for persona2 in data_rela:
                        if persona1['codigo'] == persona2['codigo']:
                            encontrado = True
                            #resultados.append(2) #actualizar
                            res =1
                            break
                    if not encontrado:
                        #resultados.append(1) #añadir
                        res=2

                datazos = data.pop('rela')
                #datazos = data.remove(data["year"])
                if len(data) > 0:
                    updated_student = await student_collection.update_one( 
                    {"_id": ObjectId(id)}, {"$set": data}
                    )
                    return True
                print(data)

            else :
                print("No hay valores insertar directo")
                updated_student = await student_collection.update_one( 
                {"_id": ObjectId(id)}, {"$set": data}
                )
            # se debe actualizar los demas campos si hubieran 
            return True
        
        else :
            print("oli")
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
