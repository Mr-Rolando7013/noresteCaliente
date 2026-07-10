import json
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from proyecto import ProyectoEcologico
from evaluador import evaluar_especie_proyecto
from ensamblador import *

# -------------------------
# 1. Definir proyecto
# -------------------------

proyecto = ProyectoEcologico(

    tipo_ecosistema="matorral_submontano",

    fase_sucesion="inicial",

    area_ha=50,

    objetivos=[
        "control_erosion",
        "captura_carbono",
        "recuperacion_habitat_fauna",
        "regulacion_microclima"
    ],

    condiciones={

        "agua": "baja",

        "humedad": "semiarido",

        "suelo": "degradado"

    },

    restricciones={

        "riego": "sin_riego"

    }
)

ORDEN_AGUA = {
    "extremadamente_baja": 0,
    "muy_baja":1,
    "baja":2,
    "baja_media": 3,
    "media":4,
    "media_alta": 5,
    "alta":6,
    "muy_alta":7
}


def generate_functional_profile(datos):
    roles_unicos = set()
    responses = []
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
                "persistencia": "",
                "etapa": "",

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
        roles_unicos.update(rol_ecologico)
        compatibilidad = data["compatibilidad_restauracion"]["objetivos"]
        refugio_fauna = data["rasgos_funcionales"]["interacciones"]["refugio_fauna"]
        estrato = data["sucesion_ecologica"]["estrato"]
        etapa = data["sucesion_ecologica"]["etapa"]
        persistencia = data["sucesion_ecologica"]["persistencia"]
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
        if etapa:
            response["rasgos_funcionales"]["etapa"] = etapa
        if persistencia:
            response["rasgos_funcionales"]["persistencia"] = persistencia
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

        responses.append(response)
    return responses

def extraccion_limpia(response):

    r = response["rol_ecologico"]
    f = response["rasgos_funcionales"]


    # -------------------------
    # Construcción de roles
    # -------------------------

    roles = set()


    for grupo in [
        r["facilitacion"],
        r["suelo"],
        r["interaccion_biologica"],
        r["ambiente"],
        r["microhabitat"]
    ]:

        roles |= {
            k for k, v in grupo.items()
            if v
        }


    # estructura también es un rol funcional
    if r["estructura"]["estructural"]:
        roles.add("estructural")


    # -------------------------
    # Perfil limpio
    # -------------------------

    binarios_ecologicos = {

        # Roles ecológicos
        "roles": roles,


        # Sucesión temprana
        "sucesion": {
            k for k, v in r["sucesion"].items()
            if v
        },


        # Estructura
        "estructura": r["estructura"]["tipo"],


        # Morfología
        "altura": f["altura_max_m"],

        "copa": f["diametro_copa_m"],


        # Recursos
        "agua": f["agua"],

        "carbono": f["captura_carbono"],


        # Ambiente
        "ambiente": {
            k for k, v in r["ambiente"].items()
            if v
        },


        # Sucesión avanzada
        "etapa": f.get(
            "etapa",
            ""
        ),

        "persistencia": f.get(
            "persistencia",
            ""
        ),


        # -------------------------
        # Compatibilidad proyecto
        # -------------------------

        "tolerancia_sequia": f["tolerancia"]["sequia"],

        "tolerancia_heladas": f["tolerancia"]["heladas"],

        "tolerancia_calor": f["tolerancia"]["calor"],

        "tolerancia_salinidad": f["tolerancia"]["salinidad"],

        "tolerancia_inundacion": f["tolerancia"]["inundacion"],

        "tolerancia_sombra": f["tolerancia"]["sombra"],


        "crecimiento": f["crecimiento"],

        "sol": f["sol"]

    }


    return binarios_ecologicos

def comp_sucesion(A, B):

    a, b = A["sucesion"], B["sucesion"]

    if not a or not b:
        return 0.6

    if "pionera" in a and "colonizadora" in b:
        return 0.95
    if "colonizadora" in a and "colonizadora_secundaria" in b:
        return 0.9

    return len(a & b) / max(len(a | b), 1)

def comp_estructura(A, B):

    diff = abs(A["altura"] - B["altura"])

    return 1 - min(diff / 10, 1)

def comp_roles(A, B):

    a,b=A["roles"],B["roles"]

    if not a or not b:
        return 0.5


    overlap=len(a&b)
    union=len(a|b)


    redundancia = overlap/union

    complementariedad = (
        len(a^b)/union
    )


    return (
        0.6*complementariedad +
        0.4*redundancia
    )

def comp_ambiente(A, B):

    a, b = A["ambiente"], B["ambiente"]

    if "riparia" in a and "xerofita" in b:
        return 0.0

    if a == b:
        return 1.0

    return 0.6

def comp_agua(A, B):

    d = abs(ORDEN_AGUA[A["agua"]] - ORDEN_AGUA[B["agua"]])

    return 1 - d/3

def score(A, B):

    return (
        0.25 * comp_sucesion(A,B) +
        0.25 * comp_estructura(A,B) +
        0.25 * comp_roles(A,B) +
        0.15 * comp_ambiente(A,B) +
        0.10 * comp_agua(A,B)
    )

def build_features(responses):
    return {
        sp["id"]: extraccion_limpia(sp)
        for sp in responses
    }

def safe_score(A, B):
    s = score(A, B)
    return max(0.0, min(1.0, s))

def build_matrix(features_map):
    ids = list(features_map.keys())

    matrix = {}

    for i in range(len(ids)):

        a_id = ids[i]
        A = features_map[a_id]

        matrix[a_id] = {}

        for j in range(i, len(ids)):

            b_id = ids[j]
            B = features_map[b_id]

            s = safe_score(A, B)

            matrix[a_id][b_id] = s

            if a_id != b_id:
                matrix[b_id] = matrix.get(b_id, {})
                matrix[b_id][a_id] = s

    return matrix

def build_graph(matrix, features_map, threshold=0.6):

    G = nx.Graph()

    for species_id, features in features_map.items():

        G.add_node(
            species_id,
            roles=list(features["roles"]),
            sucesion=list(features["sucesion"]),
            ambiente=list(features["ambiente"]),
            altura=features["altura"],
            agua=features["agua"],
            carbono=features["carbono"]
        )

    for a in matrix:
        for b, w in matrix[a].items():

            if a != b and w > threshold:
                G.add_edge(a, b, weight=w)

    return G

def especies_nucleo(G):

    centralidad = nx.degree_centrality(G)

    return sorted(
        centralidad.items(),
        key=lambda x:x[1],
        reverse=True
    )

def especies_puente(G):

    puente = nx.betweenness_centrality(
        G,
        weight="weight"
    )

    return sorted(
        puente.items(),
        key=lambda x:x[1],
        reverse=True
    )

def encontrar_comunidades(G):

    comunidades = greedy_modularity_communities(
        G,
        weight="weight"
    )

    return comunidades

def redundancia_funcional(G):

    resultado={}

    for nodo in G.nodes:

        roles_G=list(
            G.nodes[nodo]["roles"]
        )

        contador=0

        for vecino in G.neighbors(nodo):

            roles_vecino=G.nodes[vecino]["roles"]

            if set(roles_G)&set(roles_vecino):
                contador+=1

        resultado[nodo]=contador


    return sorted(
        resultado.items(),
        key=lambda x:x[1],
        reverse=True
    )

def debug_score(A, B):

    print("SUCECION:", comp_sucesion(A,B))
    print("ESTRUCTURA:", comp_estructura(A,B))
    print("ROLES:", comp_roles(A,B))
    print("AMBIENTE:", comp_ambiente(A,B))
    print("AGUA:", comp_agua(A,B))

    total = (
        0.25 * comp_sucesion(A,B) +
        0.25 * comp_estructura(A,B) +
        0.25 * comp_roles(A,B) +
        0.15 * comp_ambiente(A,B) +
        0.10 * comp_agua(A,B)
    )

    print("TOTAL:", total)



def rankear_especies(proyecto, features_map):

    resultados = []


    for especie_id, especie in features_map.items():

        score = evaluar_especie_proyecto(
            especie,
            proyecto
        )

        resultados.append({
            "id": especie_id,
            "score": score
        })


    resultados.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    return resultados

def imprimir_resumen_red(G):

    print("\n======================")
    print("RED ECOLÓGICA")
    print("======================")

    print(
        "Especies:",
        G.number_of_nodes()
    )

    print(
        "Relaciones:",
        G.number_of_edges()
    )



    print("\n======================")
    print("ESPECIES NÚCLEO")
    print("======================")


    for especie, valor in especies_nucleo(G):

        print(
            especie,
            round(valor,3)
        )



    print("\n======================")
    print("ESPECIES PUENTE")
    print("======================")


    for especie, valor in especies_puente(G):

        print(
            especie,
            round(valor,3)
        )



    print("\n======================")
    print("COMUNIDADES")
    print("======================")


    for i,c in enumerate(
        encontrar_comunidades(G)
    ):

        print(
            f"Grupo {i+1}:",
            c
        )



    print("\n======================")
    print("REDUNDANCIA FUNCIONAL")
    print("======================")


    for especie, valor in redundancia_funcional(G):

        print(
            especie,
            valor
        )

def imprimir_ranking(ranking):

    print("\n======================")
    print("RANKING ECOLÓGICO")
    print("======================")


    for r in ranking:

        print(
            r["id"],
            r["score"]
        )

def main():

    # =========================
    # 1. Cargar especies
    # =========================

    with open("./arbolesDataV2.json") as f:

        data = json.load(f)



    # =========================
    # 2. Perfil funcional
    # =========================

    responses = generate_functional_profile(
        data
    )


    features_map = build_features(
        responses
    )



    # =========================
    # 3. Construcción red ecológica
    # =========================

    matrix = build_matrix(
        features_map
    )


    G = build_graph(
        matrix,
        features_map,
        threshold=0.6
    )



    # =========================
    # 4. Análisis red
    # =========================

    imprimir_resumen_red(
        G
    )



    # =========================
    # 5. Ranking ecológico
    # =========================

    ranking = rankear_especies(
        proyecto,
        features_map
    )


    imprimir_ranking(
        ranking
    )

    comunidad = seleccionar_comunidad(
        ranking,
        features_map,
        proyecto,
        G,
        cantidad=10
    )

    plan = planificar_sucesion(
        comunidad,
        features_map
    )


    print("======================")
    print("PLAN SUCESIONAL")
    print("======================")


    for fase, especies in plan.items():

        print("\n" + fase)

        for especie in especies:

            print(
                especie
            )

    print("\n======================")
    print("COMUNIDAD PROPUESTA")
    print("======================")


    for especie in comunidad:

        print(especie)




if __name__ == "__main__":

    main()