from flask import Flask, Blueprint, render_template
import requests
import random
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env

app = Flask(__name__)

main = Blueprint('main', __name__)

frases_motivadoras = [
    "El único límite a nuestros logros de mañana está en nuestras dudas de hoy.",
    "La persistencia puede cambiar el fracaso en un éxito extraordinario.",
    "El poder no te es dado, tienes que tomarlo.",
    "Sé valiente. Toma riesgos. Nada puede sustituir la experiencia.",
    "El éxito no es el final, el fracaso no es fatal: es el coraje para continuar lo que cuenta.",
    "Cree en ti mismo y en todo lo que eres. Sepa que hay algo dentro de ti que es más grande que cualquier obstáculo.",
    "Actúa como si lo que haces marca la diferencia. Lo hace.",
    "Nunca es demasiado tarde para ser lo que podrías haber sido.",
    "Haz que tu vida sea un sueño, y un sueño, una realidad.",
    "No esperes a que las oportunidades lleguen. Créelas.",
    "Todo lo que siempre has querido está del otro lado del miedo.",
    "El futuro pertenece a aquellos que creen en la belleza de sus sueños.",
    "El éxito no se logra sólo con cualidades especiales. Es sobre todo un trabajo de constancia, de método y de organización.",
    "Para ser exitoso, tu deseo de éxito debe ser mayor que tu miedo al fracaso.",
    "Lo imposible es el fantasma de los tímidos y el refugio de los cobardes.",
    "No cuentes los días, haz que los días cuenten.",
    "No se trata de no caerse, sino de levantarse siempre."
]

api_key = os.getenv('GIPHY_API_KEY')
giphy_url = 'https://api.giphy.com/v1/gifs/random'

@main.route('/')
def home():
    frase = random.choice(frases_motivadoras)
    params = {'api_key': api_key, 'tag': 'motivation', 'rating': 'G'}
    response = requests.get(giphy_url, params=params)
    data = response.json()

    # Imprimir la estructura de los datos para depuración
    print(data)

    try:
        gif_url = data['data']['images']['original']['url']
    except (TypeError, KeyError, IndexError) as e:
        # Manejar el error y usar un valor predeterminado si ocurre un problema
        print(f"Error accediendo al GIF: {e}")
        gif_url = "URL_DEL_GIF_PREDETERMINADO"

    return render_template('index.html', frase=frase, gif_url=gif_url)

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
