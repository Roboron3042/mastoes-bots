import csv
import random
import plotly.graph_objects as go
import requests
from requests import RequestException

DATASET = '/home/mastodon/mastoes-bots/callejero-facha/DATASET.csv'
GENERO = ['placa', 'cruz', 'inscripción', 'vidriera', 'columna', 'sala biblioteca',
          'calle', 'placa alcantarilla', 'lápida', 'placa conmemorativa']

def generate_posts():
    with open(DATASET, encoding='utf8') as csvfile:
        datos = []
        objetos = set()
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        cuenta = 0
        for row in reader:
            cuenta += 1
            try:
                if ('Resignificado' not in row['ESTADO'] and
                        'etirad' not in row['ESTADO'] and
                        'Tapado' not in row['ESTADO'] and
                        'ESTADO' not in row['ESTADO'] and
                        'Placa' not in row['TIPO DE SÍMBOLO']):
                    objeto = row['CARACTERÍSTICA DE SÍMBOLO'].lower().replace('nomenclatura ', '').replace('placa calle', 'placa').replace('placa vivienda', 'placa')
                    municipio = row['MUNICIPIO'].split('/')[1] if '/' in row['MUNICIPIO'] else row['MUNICIPIO']
                    provincia = row['PROVINCIA'].split(' / ')[1] if '/' in row['PROVINCIA'] else row['PROVINCIA']
                    datos.append((
                        cuenta,
                        objeto,
                        row['DIRECCIÓN'],
                        municipio,
                        provincia,
                        row['FUENTE'],
                        float(row['LATITUD'].replace(',','')),
                        float(row['LONGITUD'].replace(',','')),
                    ))
                    objetos.add(objeto)
            except ValueError:
                pass

    # print(f"Guardados: {len(datos)} registros")
    # print(f"Tipos de objetos:")
    # print(', '.join(objetos))

    id, objeto, direccion, municipio, provincia, fuente, latitud, longitud = random.choice(datos)

    # print('Elegido:')
    # print(id)
    # print(objeto)
    # print(direccion)
    # print(municipio)
    # print(provincia)
    # print(fuente)
    # print(latitud)
    # print(longitud)

    if objeto == 'municipio':
        mensaje = (f"{municipio} ({provincia})"
                   f" aún mantiene su nombre franquista.")
    elif objeto == 'calle':
        mensaje = (f"En {municipio}{' (' + provincia + ')' if municipio != provincia else ''}"
                   f" aún existe esta calle franquista: {direccion}")
    else:
        mensaje = (f"En este lugar de {municipio}{' (' + provincia + ')' if municipio != provincia else ''}"
                   f" aún existe {'una' if objeto in GENERO else 'un'} {objeto} franquista. "
                   f"Dirección: {direccion}")

    if fuente:
        try:
            resp = requests.head(fuente, allow_redirects=True)
            if resp.status_code == 200:
                print(f'Fuente original: {fuente}')
            else:
                print(f"Fuente original status {resp.status_code}: {fuente}")
                resp = requests.get(f"https://archive.org/wayback/available?url={fuente}")
                if resp.status_code == 200:
                    arch = resp.json()
                    if ("archived_snapshots" in arch and "closest" in arch['archived_snapshots']
                            and arch['archived_snapshots']["closest"]["available"]):
                        fuente = arch['archived_snapshots']["closest"]["url"]
                        print(f'Fuente archive: {fuente}')
                    else:
                        print('Archive no disponible')
                        fuente = None
                else:
                    print(f"Archive status: {resp.status_code}")
                    fuente = None
        except RequestException as ex:
            print(ex)
            fuente = None

    fuente2 = f"https://www.deberiadesaparecer.com/explora/{id}"
    print(f"Fuente secundaria: {fuente2}")
    mapa = f"https://www.openstreetmap.org/#map=18/{latitud}/{longitud}"

    salto = '\n'
    mensaje += (f"{salto}{'Fuente:' if not fuente else 'Fuentes:'}{salto}{fuente2}{salto+fuente if fuente else ''}{salto}"
                f"Mapa:{salto}{mapa}{salto}"
                f"#MemoriaHistórica #fascismo #{municipio.replace(' ','')}{' #' + provincia.replace(' ','') if municipio != provincia else ''}")

    fig = go.Figure(go.Scattermap(
        lat=[latitud],
        lon=[longitud],
        mode='markers',
        marker=dict(symbol="circle", size=30)
    ))
    fig.update_layout(
        map=dict(
            style="open-street-map",
            center=dict(lat=latitud, lon=longitud),
            zoom=16
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0}  # Márgenes para que el mapa ocupe todito el marco
    )
    img = fig.to_image('png')

    print(mensaje)

    return [
        {
            'text': mensaje,
            'media': [
                {
                    'img': img,
                    'mime': 'image/png',
                    'alt': f"Mapa de la zona de {municipio}. Se indica con un marcador el lugar en cuestión."
                },
            ]
        },
    ]

