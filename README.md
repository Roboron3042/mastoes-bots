# Bots de masto.es

Aquí se encuentra el código de los bots que se utilizan en masto.es para ayudar con tareas de administración como guiar a los nuevos usuarios, ofrecer funciones adicionales o simplemente servir de pasatiempo.

## Apreciabot
Envía un mensaje directo (visibilidad "sólo cuentas mencionadas") a @apreciabot@masto.es incluyendo el usuario que quieres apreciar con el formato "usuario@servidor" (excluyendo el primer "@" para evitar mencionarlo). Añade "croqueta" al final para activar el modo croqueta.

Basado en el Niceness Bot https://botsin.space/@nicenessbot

## Bienvenibot
Revisa las notificaciones de un usuario con los privilegios suficientes para buscar nuevos registros y envía un mensaje de bienvenida.


## Requisitos
- Python 3
- Mastodon.py https://github.com/halcy/Mastodon.py
- Apreciabot: bs4


## Tranlations format

Use the custom_message.json file to enter a dictionary of languagues with custom messages. You can use to translate or to customize the bots. The same keys in the root of the file (in the example 'es') should be used as the option language in the command line or the configuration file.
