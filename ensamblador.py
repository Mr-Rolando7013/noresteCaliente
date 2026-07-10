from collections import defaultdict
from comparador import score

NECESIDADES_ECOSISTEMA = {


"inicial": {

    "recuperacion": {

        "pionera": 3,
        "nodriza": 3,
        "fijadora_suelo": 2,
        "ingeniera_ecosistema": 2

    },


    "estructura": {

        "estructural": 3

    },


    "fauna": {

        "frugifera": 2,
        "hospedera": 2,
        "refugio_fauna": 2

    }

}

}

import networkx as nx


def valor_red(
    especie_id,
    G
):

    if especie_id not in G:

        return 0


    centralidad = nx.betweenness_centrality(
        G
    )


    return centralidad.get(
        especie_id,
        0
    )

def seleccionar_comunidad(
    ranking,
    features_map,
    proyecto,
    G,
    cantidad=10
):

    comunidad = []


    disponibles = [
        x["id"]
        for x in ranking
    ]


    scores_proyecto = {
        x["id"]: x["score"]
        for x in ranking
    }



    while len(comunidad) < cantidad:


        mejor_especie = None
        mejor_score = -999



        cobertura_actual = evaluar_cobertura_comunidad(
            comunidad,
            features_map
        )


        score_actual = score_cobertura(
            cobertura_actual
        )



        for especie_id in disponibles:


            if especie_id in comunidad:
                continue



            prueba = comunidad + [
                especie_id
            ]



            nueva_cobertura = evaluar_cobertura_comunidad(
                prueba,
                features_map
            )


            nuevo_score = score_cobertura(
                nueva_cobertura
            )



            mejora_funcional = (
                nuevo_score - score_actual
            )



            compatibilidad = scores_proyecto.get(
                especie_id,
                0
            )



            red = valor_red(
                especie_id,
                G
            )



            redundancia = calcular_redundancia(
                especie_id,
                comunidad,
                features_map
            )



            score_final = (

                compatibilidad * 0.40

                +

                mejora_funcional * 0.35

                +

                red * 0.15

                -

                redundancia * 0.10

            )



            if score_final > mejor_score:

                mejor_score = score_final

                mejor_especie = especie_id



        if mejor_especie is None:
            break



        comunidad.append(
            mejor_especie
        )


    return comunidad

def distancia_funcional(A, B):

    return 1 - score(A,B)

def calcular_redundancia(
    especie_id,
    comunidad,
    features_map
):


    if not comunidad:

        return 0



    especie = features_map[especie_id]


    similitudes = []



    for otra_id in comunidad:


        otra = features_map[otra_id]


        similitudes.append(

            score(
                especie,
                otra
            )

        )



    return sum(similitudes) / len(similitudes)

def evaluar_cobertura_comunidad(
    comunidad,
    features_map
):

    cobertura = {

        "sucesion": set(),

        "suelo": set(),

        "estructura": set(),

        "fauna": set(),

        "microhabitat": set()

    }



    for especie_id in comunidad:


        especie = features_map[especie_id]


        roles = especie["roles"]


        # sucesión

        cobertura["sucesion"].update(
            especie["sucesion"]
        )


        # estructura

        if especie["estructura"]:

            cobertura["estructura"].add(
                especie["estructura"]
            )



        # suelo

        for rol in [
            "fijadora_suelo",
            "fijadora_nitrogeno",
            "control_erosion"
        ]:

            if rol in roles:

                cobertura["suelo"].add(
                    rol
                )



        # fauna

        for rol in [
            "frugifera",
            "hospedera",
            "refugio_fauna",
            "atrayente_fauna"
        ]:

            if rol in roles:

                cobertura["fauna"].add(
                    rol
                )



        # microhábitat

        for rol in [
            "generadora_microclima",
            "generadora_microhabitat"
        ]:

            if rol in roles:

                cobertura["microhabitat"].add(
                    rol
                )


    return cobertura

def score_cobertura(
    cobertura
):

    pesos = {

        "sucesion": 0.20,

        "suelo": 0.25,

        "estructura": 0.25,

        "fauna": 0.20,

        "microhabitat": 0.10

    }


    score = 0


    for categoria, peso in pesos.items():


        if cobertura[categoria]:

            score += peso



    return score

def planificar_sucesion(
    comunidad,
    features_map
):

    fases = {
        "FASE 1 - Establecimiento": [],
        "FASE 2 - Consolidacion": [],
        "FASE 3 - Madurez": []
    }


    for especie_id in comunidad:

        especie = features_map[especie_id]

        roles = especie["roles"]
        sucesion = especie["sucesion"]

        etapa = especie.get(
            "etapa",
            ""
        )

        persistencia = especie.get(
            "persistencia",
            ""
        )

        altura = especie.get(
            "altura",
            0
        )


        puntos = {
            "fase1": 0,
            "fase2": 0,
            "fase3": 0
        }



        # =========================
        # FASE 1
        # Establecimiento
        # =========================

        if "pionera" in sucesion:
            puntos["fase1"] += 5


        if "colonizadora" in sucesion:
            puntos["fase1"] += 4


        # combinación típica de especies fundadoras

        if (
            "pionera" in sucesion
            and
            "colonizadora" in sucesion
        ):
            puntos["fase1"] += 5


        if "nodriza" in roles:
            puntos["fase1"] += 2


        if "facilitadora" in roles:
            puntos["fase1"] += 1


        if "xerofita" in roles:
            puntos["fase1"] += 1



        # -------------------------
        # Penalizaciones
        # -------------------------

        # especies estructurales normalmente
        # llegan después de la colonización

        if "estructural" in roles:
            puntos["fase1"] -= 4


        if "especie_clave" in roles:
            puntos["fase1"] -= 2



        # árboles medianos/grandes
        # suelen ser consolidadores

        if especie.get("estructura") in [
            "arbol",
            "arbol_arbusto"
        ]:

            if altura and altura >= 8:
                puntos["fase1"] -= 2




        # =========================
        # FASE 2
        # Consolidación
        # =========================

        if "estructural" in roles:
            puntos["fase2"] += 3


        if "ingeniera_ecosistema" in roles:
            puntos["fase2"] += 2


        if "refugio_fauna" in roles:
            puntos["fase2"] += 2


        if "frugifera" in roles:
            puntos["fase2"] += 1


        if etapa == "media":
            puntos["fase2"] += 4


        if especie.get("estructura") == "arbol_arbusto":
            puntos["fase2"] += 1


        if altura and altura >= 10:
            puntos["fase2"] += 1



        # especies pioneras importantes
        # también pueden consolidar

        if (
            "pionera" in sucesion
            and
            "colonizadora" in sucesion
        ):
            puntos["fase2"] += 1




        # =========================
        # FASE 3
        # Madurez
        # =========================

        if etapa == "tardia":
            puntos["fase3"] += 6


        if persistencia == "permanente":
            puntos["fase3"] += 3


        if "especie_clave" in roles:
            puntos["fase3"] += 3


        if "hospedera" in roles:
            puntos["fase3"] += 2


        if especie.get("estructura") == "arbol":

            if altura and altura >= 20:
                puntos["fase3"] += 3




        # =========================
        # Correcciones ecológicas
        # =========================


        # especies tardías nunca deberían
        # competir con establecimiento

        if etapa == "tardia":

            puntos["fase3"] += 3
            puntos["fase1"] -= 5



        # permanentes no son colonizadoras puras

        if persistencia == "permanente":

            puntos["fase1"] -= 1




        # =========================
        # Selección final
        # =========================

        fase = max(
            puntos,
            key=puntos.get
        )


        if fase == "fase1":

            fases[
                "FASE 1 - Establecimiento"
            ].append(
                especie_id
            )


        elif fase == "fase2":

            fases[
                "FASE 2 - Consolidacion"
            ].append(
                especie_id
            )


        else:

            fases[
                "FASE 3 - Madurez"
            ].append(
                especie_id
            )


    return fases