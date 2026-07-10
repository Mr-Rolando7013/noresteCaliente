ORDEN_AGUA = {
    "extremadamente_baja": 0,
    "muy_baja": 1,
    "baja": 2,
    "baja_media": 3,
    "media": 4,
    "media_alta": 5,
    "alta": 6,
    "muy_alta": 7
}


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

    a, b = A["roles"], B["roles"]

    overlap = len(a & b)
    union = len(a | b)

    return 1 - (overlap / max(union,1))



def comp_ambiente(A, B):

    a, b = A["ambiente"], B["ambiente"]

    if "riparia" in a and "xerofita" in b:
        return 0.0

    if a == b:
        return 1.0

    return 0.6



def comp_agua(A,B):

    d = abs(
        ORDEN_AGUA[A["agua"]]
        -
        ORDEN_AGUA[B["agua"]]
    )

    return 1 - d/3



def score(A,B):

    return (

        0.25 * comp_sucesion(A,B)

        +

        0.25 * comp_estructura(A,B)

        +

        0.25 * comp_roles(A,B)

        +

        0.15 * comp_ambiente(A,B)

        +

        0.10 * comp_agua(A,B)

    )



def safe_score(A,B):

    s = score(A,B)

    return max(
        0.0,
        min(1.0,s)
    )