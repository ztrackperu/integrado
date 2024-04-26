import json
from server.database import collection
from bson import regex


collection_define ="conceptos_ot"
concepto_ot_collection = collection(collection_define)
invmae_collection = collection("invmae")
pedicab_collection = collection("pedicab")
promae_collection = collection("promae")
# helpers

#esta es la estructura esperda que se imprime como resultado

def insumo_data(concepto_ot) -> dict: 
    #print(concepto_ot["rela"])
    return {
        #no incluiremos el _id 
        "nombre": concepto_ot["IN_ARTI"],
        "codigo": concepto_ot["IN_CODI"],
        "costo": concepto_ot["IN_COST"],
        "medida":concepto_ot.get("IN_UVTA",None),
        #Lista puede ser nula
        "moneda":  concepto_ot.get("IN_MONE",None),
    }
def insumo_helper(concepto_ot) -> dict: 
    #print(concepto_ot["rela"])
    return {
        #no incluiremos el _id 
        "IN_CODI": concepto_ot["IN_CODI"],
        "IN_ARTI": concepto_ot["IN_ARTI"],
        "IN_UVTA": concepto_ot["IN_UVTA"],
        "IN_COST":concepto_ot.get("IN_COST",None),
        #Lista puede ser nula
        "IN_STOK":  concepto_ot.get("IN_STOK",None),
    }
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
        "id": concepto_ot["codigo"],
        "text" : concepto_ot["descripcion"]
    }

def insumos_helper_regex(concepto_ot) -> dict: 
    #print(concepto_ot["rela"])
    return {
        "id": concepto_ot["IN_CODI"],
        "text" : concepto_ot["IN_ARTI"]
    }

def cotizacion_helper_regex(concepto_ot) -> dict: 
    #print(concepto_ot["rela"])
    return {
        "id": concepto_ot["c_numped"],
        "text" : concepto_ot["c_numped"] +" | "+concepto_ot["c_nomcli"]
    }
#proveedor_helper_regex

def proveedor_helper_regex(concepto_ot) -> dict: 
    #print(concepto_ot["rela"])
    return {
        "id": concepto_ot["PR_NRUC"],
        "text" : concepto_ot["PR_RAZO"]
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
    print(id)
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
async def regex_concepto_ot(des:str) :
    concepto_ots = []
    print(des)
    #reg = "/^"+des+"$/i"
    #reg = "conver"
    #print(reg)
    async for concepto_ot in concepto_ot_collection.find({"$and":[{"estado":1},{"descripcion":{'$regex':des,"$options" : 'i'}}]}).limit(10):
        print(concepto_ot)
        concepto_ots.append(concepto_ot_helper_regex(concepto_ot))
    return concepto_ots
#,{"descripcion":regex.Regex(reg) }
#{"$and":[{"estado":1},{"descripcion":regex.Regex(reg) }]}
#regex.Regex.from_native(re.compile(".*"))
#{"$and":[{"estado":1},{"descripcion":regex.Regex.from_native(re.compile(".*"))}]}
#{"descripcion":regex.Regex.from_native(re.compile(reg))}


async def regex_insumo(des:str) :
    concepto_ots = []
    print(des)
    async for concepto_ot in invmae_collection.find({"$and":[{"IN_ARTI":{'$regex':des,"$options" : 'i'}}]}).limit(30):
        print(concepto_ot)
        concepto_ots.append(insumos_helper_regex(concepto_ot))
    return concepto_ots

#validarInsumo

async def validar_insumo_ot(data: dict):
    if len(data) < 1:
        return False
    concepto_ots = []
    men = data['data']
    #crear cadena para consulta
    cadena = '{"$or":['
    for number in men:
        print(number['id'])
        cadena += '{"IN_CODI":"'+number['id']+'"},'
    cadena = cadena[:-1]
    cadena +=']}'
    print(cadena)
    cadena =json.loads(cadena)
    print(cadena)
    #construir un objetivo 
    async for concepto_ot in invmae_collection.find(cadena):
        concepto_ots.append(insumo_helper(concepto_ot))
    print(concepto_ots)
    return concepto_ots

#{"$or":[{"estado":1},{"estado":0}]}
async def codigo_insumo(des:str) :
    concepto_ot = await invmae_collection.find_one({"IN_CODI":des})
    if concepto_ot:
        return insumo_data(concepto_ot) 
    #regex_cotizacion

async def regex_cotizacion(des:str) :
    concepto_ots = []
    print(des)
    async for concepto_ot in pedicab_collection.find({"$and":[{"c_numped":{'$regex':des,"$options" : 'i'}}]}).limit(30):
        print(concepto_ot)
        concepto_ots.append(cotizacion_helper_regex(concepto_ot))
    return concepto_ots

async def regex_proveedores(des:str) :
    concepto_ots = []
    print(des)
    async for concepto_ot in promae_collection.find({"$and":[{"PR_RAZO":{'$regex':des,"$options" : 'i'}}]}).limit(30):
        print(concepto_ot)
        concepto_ots.append(proveedor_helper_regex(concepto_ot))
    return concepto_ots


#viene de la api anterior 
tab_unid = collection("tab_unid")
dettabla = collection("dettabla")

async def ListaUnidadMedidaF() :
    pip = [
        {"$project":{"_id":0,"TU_CODI":1,"TU_DESC":1}},
    ]
    item_details = tab_unid.aggregate(pip)
    content1=[]
    for item in item_details :
        content1.append(item)
    return content1

async def ListaSolicitanteOTF():
    pip = [
        {"$match": {"C_CODTAB": "UOT","C_ESTADO":1,"C_TIPITM":"S"}},  
        {"$project":{"_id":0,"C_NUMITM":1,"C_DESITM":1}},        
    ]
    item_details = dettabla.aggregate(pip)
    content1=[]
    for item in item_details :
        content1.append(item)
    return content1


async def ListaSupervisadoOTF():
    pip = [
        {"$match": {"C_CODTAB": "UOT","C_ESTADO":1,"C_ABRITM":"U"}},  
        {"$project":{"_id":0,"C_NUMITM":1,"C_DESITM":1}},        
    ]
    item_details = dettabla.aggregate(pip)
    content1=[]
    for item in item_details :
        content1.append(item)   
    return content1    

async def ListaFormaPagoMF():
    pip = [
        {"$match": {"C_CODTAB": "CPO","C_ESTADO":1}},  
        {"$project":{"_id":0,"C_NUMITM":1,"C_DESITM":1}},        
    ]
    item_details = dettabla.aggregate(pip)
    content1=[]
    for item in item_details :
        content1.append(item)
import json
from server.database import collection
from bson import regex


collection_define ="conceptos_ot"
concepto_ot_collection = collection(collection_define)
invmae_collection = collection("invmae")
pedicab_collection = collection("pedicab")
promae_collection = collection("promae")
# helpers

#esta es la estructura esperda que se imprime como resultado

def insumo_data(concepto_ot) -> dict: 
    #print(concepto_ot["rela"])
    return {
        #no incluiremos el _id 
        "nombre": concepto_ot["IN_ARTI"],
        "codigo": concepto_ot["IN_CODI"],
        "costo": concepto_ot["IN_COST"],
        "medida":concepto_ot.get("IN_UVTA",None),
        #Lista puede ser nula
        "moneda":  concepto_ot.get("IN_MONE",None),
    }
def insumo_helper(concepto_ot) -> dict: 
    #print(concepto_ot["rela"])
    return {
        #no incluiremos el _id 
        "IN_CODI": concepto_ot["IN_CODI"],
        "IN_ARTI": concepto_ot["IN_ARTI"],
        "IN_UVTA": concepto_ot["IN_UVTA"],
        "IN_COST":concepto_ot.get("IN_COST",None),
        #Lista puede ser nula
        "IN_STOK":  concepto_ot.get("IN_STOK",None),
    }
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
        "id": concepto_ot["codigo"],
        "text" : concepto_ot["descripcion"]
    }

def insumos_helper_regex(concepto_ot) -> dict: 
    #print(concepto_ot["rela"])
    return {
        "id": concepto_ot["IN_CODI"],
        "text" : concepto_ot["IN_ARTI"]
    }

def cotizacion_helper_regex(concepto_ot) -> dict: 
    #print(concepto_ot["rela"])
    return {
        "id": concepto_ot["c_numped"],
        "text" : concepto_ot["c_numped"] +" | "+concepto_ot["c_nomcli"]
    }
#proveedor_helper_regex

def proveedor_helper_regex(concepto_ot) -> dict: 
    #print(concepto_ot["rela"])
    return {
        "id": concepto_ot["PR_NRUC"],
        "text" : concepto_ot["PR_RAZO"]
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
    print(id)
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
async def regex_concepto_ot(des:str) :
    concepto_ots = []
    print(des)
    #reg = "/^"+des+"$/i"
    #reg = "conver"
    #print(reg)
    async for concepto_ot in concepto_ot_collection.find({"$and":[{"estado":1},{"descripcion":{'$regex':des,"$options" : 'i'}}]}).limit(10):
        print(concepto_ot)
        concepto_ots.append(concepto_ot_helper_regex(concepto_ot))
    return concepto_ots
#,{"descripcion":regex.Regex(reg) }
#{"$and":[{"estado":1},{"descripcion":regex.Regex(reg) }]}
#regex.Regex.from_native(re.compile(".*"))
#{"$and":[{"estado":1},{"descripcion":regex.Regex.from_native(re.compile(".*"))}]}
#{"descripcion":regex.Regex.from_native(re.compile(reg))}


async def regex_insumo(des:str) :
    concepto_ots = []
    print(des)
    async for concepto_ot in invmae_collection.find({"$and":[{"IN_ARTI":{'$regex':des,"$options" : 'i'}}]}).limit(30):
        print(concepto_ot)
        concepto_ots.append(insumos_helper_regex(concepto_ot))
    return concepto_ots

#validarInsumo

async def validar_insumo_ot(data: dict):
    if len(data) < 1:
        return False
    concepto_ots = []
    men = data['data']
    #crear cadena para consulta
    cadena = '{"$or":['
    for number in men:
        print(number['id'])
        cadena += '{"IN_CODI":"'+number['id']+'"},'
    cadena = cadena[:-1]
    cadena +=']}'
    print(cadena)
    cadena =json.loads(cadena)
    print(cadena)
    #construir un objetivo 
    async for concepto_ot in invmae_collection.find(cadena):
        concepto_ots.append(insumo_helper(concepto_ot))
    print(concepto_ots)
    return concepto_ots

#{"$or":[{"estado":1},{"estado":0}]}
async def codigo_insumo(des:str) :
    concepto_ot = await invmae_collection.find_one({"IN_CODI":des})
    if concepto_ot:
        return insumo_data(concepto_ot) 
    #regex_cotizacion

async def regex_cotizacion(des:str) :
    concepto_ots = []
    print(des)
    async for concepto_ot in pedicab_collection.find({"$and":[{"c_numped":{'$regex':des,"$options" : 'i'}}]}).limit(30):
        print(concepto_ot)
        concepto_ots.append(cotizacion_helper_regex(concepto_ot))
    return concepto_ots

async def regex_proveedores(des:str) :
    concepto_ots = []
    print(des)
    async for concepto_ot in promae_collection.find({"$and":[{"PR_RAZO":{'$regex':des,"$options" : 'i'}}]}).limit(30):
        #print(concepto_ot)
        concepto_ots.append(proveedor_helper_regex(concepto_ot))
    return concepto_ots


#viene de la api anterior 
tab_unid = collection("tab_unid")
dettabla = collection("dettabla")
tab_pago = collection("tab_pago")

async def ListaUnidadMedidaF() :
    pip = [
        {"$project":{"_id":0,"TU_CODI":1,"TU_DESC":1}},
    ]
    concepto_ots = []
    async for concepto_ot in tab_unid.aggregate(pip):
        #print(concepto_ot)
        concepto_ots.append(concepto_ot)
    return concepto_ots

async def ListaSolicitanteOTF():
    pip = [
        {"$match": {"C_CODTAB": "UOT","C_ESTADO":1,"C_TIPITM":"S"}},  
        {"$project":{"_id":0,"C_NUMITM":1,"C_DESITM":1}},        
    ]
    concepto_ots = []
    async for concepto_ot in dettabla.aggregate(pip):
        #print(concepto_ot)
        concepto_ots.append(concepto_ot)
    return concepto_ots


async def ListaSupervisadoOTF():
    pip = [
        {"$match": {"C_CODTAB": "UOT","C_ESTADO":1,"C_ABRITM":"U"}},  
        {"$project":{"_id":0,"C_NUMITM":1,"C_DESITM":1}},        
    ]
    item_details = dettabla.aggregate(pip)
    concepto_ots = []
    async for concepto_ot in dettabla.aggregate(pip):
        #print(concepto_ot)
        concepto_ots.append(concepto_ot)
    return concepto_ots  

async def ListaFormaPagoMF():
    pip = [
        {"$match": {"C_CODTAB": "CPO","C_ESTADO":1}},  
        {"$project":{"_id":0,"C_NUMITM":1,"C_DESITM":1}},        
    ]
    concepto_ots = []
    async for concepto_ot in dettabla.aggregate(pip):
        #print(concepto_ot)
        concepto_ots.append(concepto_ot)
    return concepto_ots 

async def ListaPlazoMF():
    pip = [
        {"$match": {"TP_ESTA": 1}},  
        {"$project":{"_id":0,"TP_CODI":1,"TP_DESC":1}},
        {"$sort":{"TP_DESC":1}}        
    ]
    concepto_ots = []
    async for concepto_ot in tab_pago.aggregate(pip):
        #print(concepto_ot)
        concepto_ots.append(concepto_ot)
    return concepto_ots   

async def ListaTecnicoOTF():
    pip = [
        {"$match": {"C_CODTAB": "UOT","C_ESTADO":1 ,"C_TIPITM":"T"}},  
        {"$project":{"_id":0,"C_NUMITM":1,"C_DESITM":1}},        
        {"$sort":{"descripcion":1}}        
    ]
    concepto_ots = []
    async for concepto_ot in dettabla.aggregate(pip):
        #print(concepto_ot)
        concepto_ots.append(concepto_ot)
    return concepto_ots  
UNIONOFICIAL = collection("UNIONOFICIAL")
async def concepto_filtrado_periodo() :
    actividad = "PINTADO GENERAL"
    pip = [
        {"$project":{"_id":0,"c_treal":1,"d_fcrea":1}},
        {"$match": {"c_treal" : actividad }}, 
        {
            "$facet" : {
                "total":[
                    {"$count" : 'total'} 
                ],
                "2015":[
                    {"$match": {"d_fcrea": {"$regex" :"/2015"},}},
                    {"$count" : '2015'} 
                ],
                "2016":[
                    {"$match": {"d_fcrea": {"$regex" :"/2016"},}},
                    {"$count" : '2016'} 
                ],
                "2017":[
                    {"$match": {"d_fcrea": {"$regex" :"/2017"},}},
                    {"$count" : '2017'} 
                ],
                "2018":[
                    {"$match": {"d_fcrea": {"$regex" :"/2018"},}},
                    {"$count" : '2018'} 
                ],
                "2019":[
                    {"$match": {"d_fcrea": {"$regex" :"/2019"},}},
                    {"$count" : '2019'} 
                ],
                "2020":[
                    {"$match": {"d_fcrea": {"$regex" :"/2020"},}},
                    {"$count" : '2020'} 
                ],
                "2021":[
                    {"$match": {"d_fcrea": {"$regex" :"/2021"},}},
                    {"$count" : '2021'} 
                ],
                "2022":[
                    {"$match": {"d_fcrea": {"$regex" :"/2022"},}},
                    {"$count" : '2022'} 
                ],
                "2023":[
                    {"$match": {"d_fcrea": {"$regex" :"/2023"},}},
                    {"$count" : '2023'} 
                ],
                "2024":[
                    {"$match": {"d_fcrea": {"$regex" :"/2024"},}},
                    {"$count" : '2024'} 
                ],      
            }
        }       
    ]
    concepto_ots = []
    async for concepto_ot in UNIONOFICIAL.aggregate(pip):
        #print(concepto_ot)
        concepto_ots.append(concepto_ot)
    return concepto_ots  