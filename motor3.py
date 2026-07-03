import json

def generate_functional_profile(datos):
    for data in datos:
        # Todo: Profundidad y expansion de raiz
        response = {
            "id": None,
            "rol_ecologico": {
                "sucesion": {
                "pionera": False,
                "colonizadora": False,
                "colonizadora_secundaria": False
                },

                "estructura": {
                "estructural": False,
                "tipo": None
                },

                "facilitacion": {
                "nodriza": False,
                "facilitadora": False,
                "ingeniera_ecosistema": False,
                "especie_clave": False
                },

                "suelo": {
                "fijadora_nitrogeno": False,
                "fijadora_suelo": False,
                "control_erosion": False
                },

                "interaccion_biologica": {
                "melifera": False,
                "frugifera": False,
                "atrayente_polinizadores": False,
                "atrayente_fauna": False,
                "refugio_fauna": False,
                "hospedera": False
                },

                "ambiente": {
                "riparia": False,
                "riparia_facultativa": False,
                "xerofita": False
                },

                "microhabitat": {
                "generadora_microclima": False,
                "generadora_microhabitat": False
                }
            },
            "rasgos_funcionales": {
                "estrato": "",

                "altura_max_m": None,

                "diametro_copa_m": None,

                "agua": "",

                "sol": "",

                "crecimiento": "",

                "captura_carbono": "",

                "tolerancia": {
                "sequia": "",
                "heladas": "",
                "calor": "",
                "salinidad": "",
                "inundacion": "",
                "sombra": ""
                }
            }
        }
        
        
        response["id"] = data["id"]
        rol_ecologico = []
        compatibilidad = []
        rol_ecologico = data.get("rol_ecologico", [])
        compatibilidad = data["compatibilidad_restauracion"]["objetivos"]
        refugio_fauna = data["rasgos_funcionales"]["interacciones"]["refugio_fauna"]
        estrato = data["sucesion_ecologica"]["estrato"]
        altura_max_m = data["morfologia"]["altura_max_m"]
        if altura_max_m:
            response["rasgos_funcionales"]["altura_max_m"] = altura_max_m

        diametro_copa_m = data["morfologia"]["diametro_copa_m"]
        if diametro_copa_m:
            response["rasgos_funcionales"]["diametro_copa_m"] = diametro_copa_m

        agua = data["ecologia"]["agua"]
        if agua:
            response["rasgos_funcionales"]["agua"] = agua

        sol = data["ecologia"]["sol"]
        if sol:
            response["rasgos_funcionales"]["sol"] = sol

        captura_carbono = data["ecologia"]["captura_carbono"]
        if captura_carbono:
            response["rasgos_funcionales"]["captura_carbono"] = captura_carbono

        sequia = data["rasgos_funcionales"]["tolerancia"]["sequia"]
        if sequia:
            response["rasgos_funcionales"]["tolerancia"]["sequia"] = sequia

        heladas = data["rasgos_funcionales"]["tolerancia"]["heladas"]
        if heladas:
            response["rasgos_funcionales"]["tolerancia"]["heladas"] = heladas
        
        calor = data["rasgos_funcionales"]["tolerancia"]["calor"]
        if calor:
            response["rasgos_funcionales"]["tolerancia"]["calor"] = calor

        salinidad = data["rasgos_funcionales"]["tolerancia"]["salinidad"]
        if salinidad:
            response["rasgos_funcionales"]["tolerancia"]["salinidad"] = salinidad

        inundacion = data["rasgos_funcionales"]["tolerancia"]["inundacion"]
        if inundacion:
            response["rasgos_funcionales"]["tolerancia"]["inundacion"] = inundacion

        sombra = data["rasgos_funcionales"]["tolerancia"]["sombra"]
        if sombra:
            response["rasgos_funcionales"]["tolerancia"]["sombra"] = sombra

        crecimiento = data["ecologia"]["crecimiento"]
        if crecimiento:
            response["rasgos_funcionales"]["crecimiento"] = crecimiento

        if estrato:
            response["rasgos_funcionales"]["estrato"] = estrato
        if refugio_fauna:
            response["rol_ecologico"]["interaccion_biologica"]["refugio_fauna"] = True

        response["rol_ecologico"]["estructura"]["tipo"] = data["tipo"]

        adaptaciones = data["adaptaciones_ecologicas"]

        for adaptacion in adaptaciones:
            if adaptacion == "xerofita":
                response["rol_ecologico"]["ambiente"]["xerofita"] = True
        
        for rol in rol_ecologico:
            if rol == "pionera":
                response["rol_ecologico"]["sucesion"]["pionera"] = True
            if rol == "colonizadora":
                response["rol_ecologico"]["sucesion"]["colonizadora"] = True
            if rol == "colonizadora_secundaria":
                response["rol_ecologico"]["sucesion"]["colonizadora_secundaria"] = True
            if rol == "estructural":
                response["rol_ecologico"]["estructura"]["estructural"] = True
            if rol == "nodriza":
                response["rol_ecologico"]["facilitacion"]["nodriza"] = True
            if rol == "facilitadora":
                response["rol_ecologico"]["facilitacion"]["facilitadora"] = True
            if rol == "ingeniera_ecosistema":
                response["rol_ecologico"]["facilitacion"]["ingeniera_ecosistema"] = True
            if rol == "especie_clave":
                response["rol_ecologico"]["facilitacion"]["especie_clave"] = True
            if rol == "fijadora_nitrogeno":
                response["rol_ecologico"]["suelo"]["fijadora_nitrogeno"] = True
            if rol == "fijadora_suelo":
                response["rol_ecologico"]["suelo"]["fijadora_suelo"] = True
            if rol == "melifera":
                response["rol_ecologico"]["interaccion_biologica"]["melifera"] = True
            if rol == "frugifera":
                response["rol_ecologico"]["interaccion_biologica"]["frugifera"] = True
            if rol == "atrayente_polinizadores":
                response["rol_ecologico"]["interaccion_biologica"]["atrayente_polinizadores"] = True
            if rol == "atrayente_fauna":
                response["rol_ecologico"]["interaccion_biologica"]["atrayente_fauna"] = True
            if rol == "hospedera":
                response["rol_ecologico"]["interaccion_biologica"]["hospedera"] = True
            if rol == "riparia":
                response["rol_ecologico"]["ambiente"]["riparia"] = True
            if rol == "riparia_facultativa":
                response["rol_ecologico"]["ambiente"]["riparia_facultativa"] = True
            if rol == "generadora_microclima":
                response["rol_ecologico"]["microhabitat"]["generadora_microclima"] = True
            if rol == "generadora_microhabitat":
                response["rol_ecologico"]["microhabitat"]["generadora_microhabitat"] = True
            
        for rol in compatibilidad:
            if rol == "control_erosion":
                response["rol_ecologico"]["suelo"]["control_erosion"] = True

    print(response)

def main():
    with open("./arbolesDataV2.json") as f:
        data = json.load(f)
    
    generate_functional_profile(data)

if __name__ == "__main__":
    main()