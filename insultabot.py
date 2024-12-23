from common import get_api, get_gender, get_new_notifications, list_read
from random import choice

articulos_indefinidos =["un", "una", "une"]
articulos_definidos = ["el", "la", "le"]
vocales_genero = ["o", "a", "e"]

mensaje_api_incompatible = "No pude acceder a la información de la cuenta remota. Probablemente esté usando otro software distinto a Mastodon. No pude comprobar si tiene relación con ARTICULO_INDEFINIDO INSULTO como tú."
mensaje_seguidores_vacio = "No pude consultar la lista de seguidos de la cuenta mencionada (tal vez está oculta o es demasiado grande). No pude comprobar si tiene relación con ARTICULO_INDEFINIDO INSULTO como tú."
mensaje_no_amigo = "La cuenta mencionada no tiene una relación de seguimiento contigo. Es comprensible que no quiera tener nada que ver con ARTICULO_INDEFINIDO INSULTO como tú."
mensaje_nobot = "La cuenta objetivo tiene la etiqueta #nobot en su biografía. ¡No tengo poder aquí, INSULTO!"
mensaje_mismo = "Hay que ser muy INSULTO para insultarse a uno mismo. Enhorabuena."
mensaje_creador = "¿Cómo te atreves a intentar insultar a mi creador, INSULTO?"
mensaje_insuficientes = "Tú, INSULTO, no has escrito suficientes menciones para insultar a nadie."
mensaje_follow = "Bienvenid0 al club, INSULTO."

mensajes = [
    "Según un prestigioso estudio de la universidad de INSULTADOR, eres ARTICULO_INDEFINIDO INSULTO, INSULTADO.",
    "Un comité de expertos liderado por INSULTADOR ha llegado a la conclusión de que INSULTADO es muy INSULTO. Y tienen razón.",
    "INSULTADO, eres un poco INSULTO, me he dado cuenta gracias a INSULTADOR. Háztelo mirar, ¿vale?",
    "¡INSULTADO, eres ARTICULO_INDEFINIDO INSULTO! ¿Lo sabías? Seguramente no, porque aunque INSULTADOR me lo haya dicho, tú eres tan INSULTO que no te das cuenta.",
    "INSULTADO que sepas que eres ARTICULO_INDEFINIDO INSULTO, como INSULTADOR ha hecho bien en señalar.",
    "INSULTADOR te concede el dudoso honor de ser ARTICULO_DEFINIDO mastodonte más INSULTO de todos, INSULTADO.",
    "A INSULTADOR le preocupa lo INSULTO que eres, INSULTADO. Pero no mucho.",
    "Todos tus amigos piensan que eres ARTICULO_INDEFINIDO INSULTO, INSULTADO. Bueno, todos todos no, pero INSULTADOR sí.",
    "Ya te vale, INSULTADO, podrías ser un poco menos INSULTO, que tienes a INSULTADOR hasta las narices.",
    "INSULTADO, si fueses un poco menos INSULTO, INSULTADOR no habría tenido que mandar este mensaje.",
    "No sabíamos que INSULTADO era ARTICULO_INDEFINIDO INSULTO, menos mal que INSULTADOR ha avisado.",
    "INSULTADO Perdona que te lo diga pero eres un poco INSULTO. INSULTADOR quería decírtelo pero no se atrevía.",
    "Después de todo INSULTADOR tenía razón, INSULTADO es ARTICULO_INDEFINIDO INSULTO.",
    "Hoy estaba de bajona, pero luego INSULTADOR me recordó lo INSULTO que es INSULTADO y se me pasó.",
    "Solo hay dos cosas ciertas en esta vida: que INSULTADO es ARTICULO_INDEFINIDO INSULTO y que esto me lo ha dicho INSULTADOR.",
    "¿Se puede ser más INSULTO que INSULTADO? Es una pregunta retórica, solo INSULTADOR conoce la respuesta.",
    "Hoy es un día perfecto para recordar a INSULTADO lo INSULTO que es. Bueno, hoy y cualquier día, siempre que esté INSULTADOR para recordármelo.",
    "¿Sabes qué hora es, INSULTADOR? ¡La hora de llamar INSULTO a INSULTADO!",
    "INSULTADO te digo que eres ARTICULO_INDEFINIDO INSULTO, y me quedo corto. Pero si quieres INSULTADOR te lo expande.",
    "INSULTADO me han pedido que te diga que eres ARTICULO_INDEFINIDO INSULTO, que no sé muy bien lo que significa, pero tiene que ser algo malo porque me lo ha dicho INSULTADOR.",
    "INSULTADO ¡INSULTO! ¡INSULTO_2! ¡INSULTO_3! ¡INSULTO_4!\n\nUff, qué ganas le tenía a esta cuenta. Gracias por la oportunidad, INSULTADOR",
    "Alguien que te aprecia mucho (INSULTADOR) quiere recordarte que eres ARTICULO_INDEFINIDO INSULTO :ablobcatheartsqueeze: ¡Sigue así, INSULTADO!",
    "En el mundo hay chorrocientos millones de seres humanos, pero solo uno tan INSULTO como tú, INSULTADO. Lo sabemos porque INSULTADOR lo ha comprobado.",
    "Cuando INSULTADOR creía que no podría encontrar a nadie más INSULTO, encontró a INSULTADO y le demostró que sí que podía.",
    "Mira, me han pedido que te insulte, INSULTADO, pero la persona que me lo ha pedido, INSULTADOR, me cae fatal y es ARTICULO_INDEFINIDO INSULTO de cuidado, así que esta vez te vas a salvar."
]

def get_insulto_inclusivo(insulto, gender):
    insulto = insulto.split(",")
    if(len(insulto) > 1):
        insulto_inclusivo = insulto[gender]
    else:
        insulto_inclusivo = insulto[0]
    return insulto_inclusivo

def insultar_insultador(insulto, insultador, status, mensaje):
    gender = get_gender(insultador)
    insulto = get_insulto_inclusivo(insulto, gender)
    mensaje = mensaje.replace("INSULTO", insulto).replace("ARTICULO_INDEFINIDO", articulos_indefinidos[gender])
    api.status_post("@" + insultador.acct + " " + mensaje.replace("INSULTO", insulto), in_reply_to_id=status.id, visibility="unlisted" )

def insultar_insultado(insulto, insultador, insultado, insultado_acct, status):
    gender = get_gender(insultado)
    insulto = get_insulto_inclusivo(insulto, gender)
    mensaje = choice(mensajes)
    mensaje = mensaje.replace("INSULTADOR", "@" + insultador.acct)
    mensaje = mensaje.replace("INSULTADO", "@" + insultado_acct)
    if("INSULTO_2" in mensaje):
        mensaje = mensaje.replace("INSULTO_2", get_insulto_inclusivo(choice(insultos), gender).capitalize() )
        mensaje = mensaje.replace("INSULTO_3", get_insulto_inclusivo(choice(insultos), gender).capitalize())
        mensaje = mensaje.replace("INSULTO_4", get_insulto_inclusivo(choice(insultos), gender).capitalize())
        mensaje = mensaje.replace("INSULTO", insulto.capitalize())
    mensaje = mensaje.replace("INSULTO", insulto)
    mensaje = mensaje.replace("ARTICULO_INDEFINIDO", articulos_indefinidos[gender])
    mensaje = mensaje.replace("ARTICULO_DEFINIDO", articulos_definidos[gender])
    reply = api.status_post(mensaje, in_reply_to_id=status.id, visibility="unlisted" )
    api.status_reblog(reply.id)

bot_name = 'insultabot'
api = get_api('masto.es', bot_name)
insultos = list_read(bot_name + "_insultos")
notifications = get_new_notifications(api, bot_name, ["mention", "follow"])

for n in notifications:
    insultador = n.account
    if(n.type == "follow"):
        choosen_insulto = choice(insultos)
        insulto = get_insulto_inclusivo(choosen_insulto, get_gender(insultador))
        api.status_post("@" + insultador.acct + " " + mensaje_follow.replace("INSULTO", insulto).replace("0",vocales_genero[get_gender(insultador)]), visibility="unlisted" )
    else:
        choosen_insulto = choice(insultos)
        menciones = n.status.mentions
        insultado_mencion = {}
        if(len(menciones) < 2):
            insulto = get_insulto_inclusivo(choosen_insulto, get_gender(insultador))
            api.status_post("@" + insultador.acct + " " + mensaje_insuficientes.replace("INSULTO", insulto), in_reply_to_id=n.status.id, visibility="unlisted" )
            break
        for mencion in menciones:
            if(mencion.url == "https://masto.es/@rober"):
                insultar_insultador(choosen_insulto, insultador, n.status, mensaje_creador)
                break
            elif(mencion.acct == insultador.acct):
                insultar_insultador(choosen_insulto, insultador, n.status, mensaje_mismo)
                break
            elif(mencion.url == "https://masto.es/@insultabot"):
                continue
            else:
                insultado_mencion = mencion
                break
        if(insultado_mencion == {}):
            break
        if("@" not in insultado_mencion.acct):
            dominio_insultado = "masto.es"
        else:
            dominio_insultado = insultado_mencion.acct.split("@")[1]
        try:
            insultado_api = get_api(dominio_insultado)
            insultado = insultado_api.account_lookup(insultado_mencion.acct)
        except:
            insultar_insultador(choosen_insulto, insultador, n.status, mensaje_api_incompatible)
            break
        if("nobot" in insultado.note):
            insultar_insultador(choosen_insulto, insultador, n.status, mensaje_nobot)
            break
        # Para evitar rate-limits, descartamos cuentas que sigan demasiada gente
        elif(insultado.following_count > 6000 or insultado.following_count == 0):
            insultar_insultador(choosen_insulto, insultador, n.status, mensaje_seguidores_vacio)
            break
        try:
            follows = insultado_api.account_following(insultado.id, limit=80)
        except:
            insultar_insultador(choosen_insulto, insultador, n.status, mensaje_api_incompatible)
            break
        if(len(follows) == 0):
            insultar_insultador(choosen_insulto, insultador, n.status, mensaje_seguidores_vacio)
            break
        else:
            follows = insultado_api.fetch_remaining(follows)
        encontrado = False
        if("@" not in insultador.acct):
            insultador_acct_compare = insultador.acct + "@masto.es"
        else:
            insultador_acct_compare = insultador.acct
        for follow in follows:
            if("@" not in follow.acct):
                follow_acct_compare = follow.acct + "@" + dominio_insultado
            else:
                follow_acct_compare = follow.acct
            if(insultador_acct_compare == follow_acct_compare):
                encontrado = True
                insultar_insultado(choosen_insulto, insultador, insultado, insultado_mencion.acct, n.status)
                break
        if(encontrado == False):
            insultar_insultador(choosen_insulto, insultador, n.status, mensaje_no_amigo)
