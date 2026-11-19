from logging.config import dictConfig

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("USDA_API_KEY")

def calcular_macros(alimento, gramos):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={alimento}&api_key={API_KEY}"
    nutrientes_interes = {
        "Energy": "calorias",
        "Protein": "proteinas",
        "Carbohydrate, by difference": "hdc",
        "Total lipid (fat)": "grasas"
    }
    respuesta = requests.get(url)
    datos = respuesta.json()
    if not datos["foods"]:
        return "Alimento no encontrado"
    nombre_alimento = datos["foods"][0]['description']
    primer_alimento = datos["foods"][0]["foodNutrients"]
    nutrientes_alimento = {}
    for nutrientes in primer_alimento:
        nombre = nutrientes["nutrientName"]
        if nombre in nutrientes_interes:
            clave = nutrientes_interes[nombre]
            nutrientes_alimento[clave] = round(nutrientes["value"]/100*gramos,2)
            if len(nutrientes_alimento) == 4:
                break
    return nutrientes_alimento

def comprobar_comida(alimento):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={alimento}&api_key={API_KEY}"
    respuesta = requests.get(url)
    datos = respuesta.json()
    if not datos["foods"]:
        return "Alimento no encontrado"
    nombre_alimento = datos["foods"][0]['description']
    isNombreAlimentoOk = input(f"Es {nombre_alimento} el alimento que estas buscando? (y/n)")
    if isNombreAlimentoOk == "y":
        return "Alimento  encontrado"
    elif isNombreAlimentoOk == "n":
        return "Alimento no encontrado"


