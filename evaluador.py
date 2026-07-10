MAPA_OBJETIVOS = {

    "control_erosion": {
        "control_erosion",
        "fijadora_suelo",
        "ingeniera_ecosistema",
        "nodriza"
    },


    "recuperacion_habitat_fauna": {
        "refugio_fauna",
        "atrayente_fauna",
        "hospedera"
    },


    "captura_carbono": {
        "estructural",
        "ingeniera_ecosistema"
    }
}

REGLAS_AMBIENTE = {

    "semiarido": {

        "favorece": {
            "xerofita"
        },

        "penaliza": {
            "riparia"
        }
    },


    "humedo": {

        "favorece": {
            "riparia"
        },

        "penaliza": {
            "xerofita"
        }
    }
}


REGLAS_SUCESION = {

    "inicial": {

        "premia": {
            "pionera",
            "colonizadora",
            "nodriza",
            "ingeniera_ecosistema"
        }

    },


    "intermedia": {

        "premia": {
            "colonizadora_secundaria",
            "facilitadora"
        }

    },


    "maduracion": {

        "premia": {
            "estructural",
            "especie_clave"
        }

    }
}

def evaluar_especie_proyecto(especie, proyecto):
    puntos_contexto = 0
    penalizaciones = 0

    # ======================
    # PUNTOS INTERNOS
    # ======================

    puntos_agua = 0
    puntos_objetivos = 0
    puntos_sequia = 0
    puntos_escala = 0


    detalles = {}


    roles = especie["roles"]


    # ======================
    # AGUA
    # ======================

    agua_especie = especie["agua"]
    agua_proyecto = proyecto.condiciones.get("agua")


    if agua_especie == agua_proyecto:

        puntos_agua = 20

    elif agua_especie and agua_proyecto:

        puntos_agua = 10


    detalles["agua"] = puntos_agua



    # ======================
    # OBJETIVOS ECOLÓGICOS
    # ======================

    objetivos = proyecto.objetivos


    for objetivo in objetivos:


        roles_necesarios = MAPA_OBJETIVOS.get(
            objetivo,
            set()
        )


        if roles & roles_necesarios:

            puntos_objetivos += 10



        # Carbono tiene evaluación adicional
        if objetivo == "captura_carbono":

            if especie["carbono"] in [
                "alta",
                "muy_alta"
            ]:

                puntos_objetivos += 10



    # máximo 40
    puntos_objetivos = min(
        puntos_objetivos,
        40
    )


    detalles["objetivos"] = puntos_objetivos



    # ======================
    # ADAPTACIÓN CLIMÁTICA
    # ======================

    tolerancia = especie["tolerancia_sequia"]


    if proyecto.restricciones.get(
        "riego"
    ) == "sin_riego":


        if tolerancia in [
            "alta",
            "muy_alta"
        ]:

            puntos_sequia = 20


        elif tolerancia:

            puntos_sequia = 10



    detalles["sequia"] = puntos_sequia



    # ======================
    # ESCALA DEL PROYECTO
    # ======================

    area = proyecto.area_ha


    roles_estructura = {

        "estructural",
        "ingeniera_ecosistema",
        "nodriza"
    }


    if area > 20:


        if roles & roles_estructura:

            puntos_escala = 20


    else:

        puntos_escala = 10



    detalles["escala"] = puntos_escala

    # ======================
    # CONTEXTO AMBIENTAL
    # ======================

    ambiente = especie["ambiente"]


    regla = REGLAS_AMBIENTE.get(
        proyecto.condiciones["humedad"]
    )


    if regla:


        if ambiente & regla["favorece"]:
            puntos_contexto += 10


        if ambiente & regla["penaliza"]:
            penalizaciones += 10



    # ======================
    # SUCESIÓN
    # ======================

    sucesion = especie["sucesion"]


    regla_sucesion = REGLAS_SUCESION.get(
        proyecto.fase_sucesion
    )


    if regla_sucesion:


        if sucesion & regla_sucesion["premia"]:
            puntos_contexto += 10

    detalles["contexto"] = puntos_contexto
    detalles["penalizacion"] = penalizaciones

    # ======================
    # SCORE FINAL
    # ======================


    score_final = (

        (puntos_agua / 20) * 0.20 +

        (puntos_objetivos / 40) * 0.35 +

        (puntos_sequia / 20) * 0.15 +

        (puntos_escala / 20) * 0.15 +

        (puntos_contexto / 20) * 0.15

    )


    score_final -= (
        penalizaciones / 100
    )


    score_final = max(
        0,
        min(
            1,
            score_final
        )
    )


    print(especie)

    print(detalles)

    print(
        "TOTAL:",
        round(score_final,3)
    )


    return round(score_final,3)