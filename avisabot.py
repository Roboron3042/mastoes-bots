from common import get_api
from common import list_append
from common import list_read

domain = "paquita.masto.host"
message = "¡Hola! Veo que sigues publicando desde el servidor de " + domain + ". "
message += "Lamentablemente, este servidor cerrará sus puertas pronto (6 de septiembre de 2025 https://paquita.masto.host/@paquita/114986868044138924), así que si quieres seguir usando Mastodon tendrás que migrar tu cuenta a otro servidor.\n\n"
message += "En el caso de Paquita, algunas de sus usuarias montaron una sucesora espiritual en https://neopaquita.es, así que esa es buena opción. Otra opción puede ser https://masto.es, el mayor servidor en español que yo mismo administro.\n\n"
message += "Te dejo con los pasos básicos para migrar una cuenta de " + domain + " a masto.es (remplaza los enlaces a masto.es con el servidor que hayas escogido si finalmente eliges otro):\n\n"
message += "1 - Crea una nueva cuenta en el nuevo servidor https://masto.es/auth/sign_up\n"
message += "2 - Pon tu cuenta anterior en https://masto.es/settings/aliases\n"
message += "3 - Pon tu cuenta nueva en https://" + domain + "/settings/migration\n"
message += "4 - Descarga tu lista de seguidos en https://" + domain + "/settings/export\n"
message += "5 - Importa tu lista de seguidos en https://masto.es/settings/imports\n\n"
message += "Si necesitas más información sobre como migrar una cuenta puedes leer el tutorial de https://sidiostedalimones.com/blog/2024/como-migrar-de-instancia/ ,¡o puedes preguntarme a mí!"

bot_name = 'avisabot'
api_mastoes = get_api('masto.es', 'rober')

avisados = list_read(bot_name)
api_external = get_api(domain)

timeline = api_external.timeline(timeline='local', limit=80)

for post in timeline:
	username = post['account']['acct'] + "@" + domain
	if username not in avisados:
		print("@" + username)
		try:
			# Puede que el usuario no permita buscar sus publicaciones
			api_mastoes.search_v2(post['url'], result_type="posts")
			api_mastoes.status_post("@" + username + " " + message, visibility="private", in_reply_to_id=local_post)
		except:
			api_mastoes.status_post("@" + username + " " + message, visibility="direct")
		list_append(bot_name, username)
		avisados.append(username)
