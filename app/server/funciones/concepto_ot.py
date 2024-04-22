import re
from server.database import collection
from bson import regex

collection_define ="conceptos_ot"
concepto_ot_collection = collection(collection_define)

# helpers

#esta es la estructura esperda que se imprime como resultado
def concepto_ot_helper(concepto_ot) -> dict: 
    #print(concepto_ot["rela"])
    return {
        #no incluiremos el _id 
        "id": concepto_ot["id"],
        "codigo": concepto_ot["codigo"],
        "descripcion": concepto_ot["descripcion"],
        "estado":concepto_ot.get("estado",None),
        #Lista puede ser nula
        "insumos":  concepto_ot.get("insumos",None),
    }

def concepto_ot_helper_validar(concepto_ot) -> dict: 
    #print(concepto_ot["rela"])
    return {
        "descripcion": concepto_ot["descripcion"]
    }
def concepto_ot_helper_regex(concepto_ot) -> dict: 
    #print(concepto_ot["rela"])
    return {
        "codigo": concepto_ot["codigo"],
        "text" : concepto_ot["descripcion"]
    }



# crud operation
# Recuperar todos los concepto_ots presentes en la base de datos.
async def retrieve_concepto_ots():
    concepto_ots = []
    async for concepto_ot in concepto_ot_collection.find({"$or":[{"estado":1},{"estado":0}]}):
        #print(concepto_ot)
        concepto_ots.append(concepto_ot_helper(concepto_ot))
    return concepto_ots


# Agregar un nuevo concepto_ot a la base de datos
async def add_concepto_ot(concepto_ot_data: dict) -> dict:
    #aqui envia el json a mongo y lo inserta
    concepto_ot = await concepto_ot_collection.insert_one(concepto_ot_data)
    #aqui busca el dato obtenido para mostrarlo como respuesta
    new_concepto_ot = await concepto_ot_collection.find_one({"_id": concepto_ot.inserted_id})
    return concepto_ot_helper(new_concepto_ot)

# Recuperar un concepto_ot con un ID coincidente
async def retrieve_concepto_ot(id: int) -> dict:
    #importante convertir a int cunado se busca a un dato por numero
    concepto_ot = await concepto_ot_collection.find_one({"id": int(id)})
    #print(concepto_ot)
    if concepto_ot:
        return concepto_ot_helper(concepto_ot) 

# Actualizar a un estudiante con un ID coincidente
async def update_concepto_ot(id: int, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    concepto_ot = await concepto_ot_collection.find_one({"id": id})
    if concepto_ot:
        updated_concepto_ot = await concepto_ot_collection.update_one(
            {"id": id}, {"$set": data}
        )
        if updated_concepto_ot:
            return True
        return False

# Eliminar un concepto_ot de la base de datos
async def delete_concepto_ot(id: int):
    concepto_ot = await concepto_ot_collection.find_one({"id": id})
    if concepto_ot:
        await concepto_ot_collection.delete_one({"id": id})
        return True
    
# Extraer el ultimo  concepto_ot de la base de datos en base al campo id
async def extraer_concepto_ot()->dict:
    concepto_ots = []
    async for concepto_ot in concepto_ot_collection.find({"$or":[{"estado":1},{"estado":0}]}).sort({"id":-1}).limit(1):
        #print(concepto_ot)
        concepto_ots.append(concepto_ot_helper(concepto_ot))
    #se debe extraer el primir resultado
    return concepto_ots[0]


# Validar  existencia  de un adescripcion en conceptosOT
async def validar_concepto_ot(data: dict):
    if len(data) < 1:
        return False
    concepto_ots = []
    async for concepto_ot in concepto_ot_collection.find({"estado":1}):
        concepto_ots.append(concepto_ot_helper_validar(concepto_ot))
    if(data in concepto_ots):
        men = "duplicado"
    else:
        men ="ok"
    return men

# Recuperar un concepto_ot con un ID coincidente
async def regex_concepto_ot(des: str) :
    concepto_ots = []
    print(des)
    #reg = "/^"+des+"$/i"
    reg = "/^re$/i"
    print(reg)
    async for concepto_ot in concepto_ot_collection.find({"$and":[{"estado":1},{"descripcion":regex.Regex.from_native(re.compile(".*"))}]}).limit(10):
        print(concepto_ot)
        concepto_ots.append(concepto_ot_helper_regex(concepto_ot))
    return concepto_ots
#,{"descripcion":regex.Regex(reg) }
#{"$and":[{"estado":1},{"descripcion":regex.Regex(reg) }]}
#regex.Regex.from_native(re.compile(".*"))
#{"$and":[{"estado":1},{"descripcion":regex.Regex.from_native(re.compile(".*"))}]}