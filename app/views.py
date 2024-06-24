# app/views.py
from flask import Blueprint, render_template, jsonify
import os
import pyodbc
import requests
import random

main = Blueprint('main', __name__)

def get_db_connection():
    server = os.getenv('SQL_SERVER', 'localhost')
    database = os.getenv('SQL_DATABASE')
    username = os.getenv('SQL_USER')
    password = os.getenv('SQL_PASSWORD')
    driver = os.getenv('SQL_DRIVER', 'ODBC Driver 17 for SQL Server')
    connection_string = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    return pyodbc.connect(connection_string)

@main.route('/get-phrase')
def get_phrase():
    cnxn = get_db_connection()
    cursor = cnxn.cursor()
    cursor.execute("SELECT TOP 1 Id, Frase FROM FrasesMotivadoras ORDER BY NEWID()")
    row = cursor.fetchone()
    frase = row[1] if row else "No hay frases disponibles."
    
    api_key = os.getenv('GIPHY_API_KEY')
    giphy_url = 'https://api.giphy.com/v1/gifs/random'
    params = {'api_key': api_key, 'tag': 'motivation', 'rating': 'G'}
    response = requests.get(giphy_url, params=params)
    data = response.json()
    gif_url = data['data']['images']['original']['url'] if data.get('data') else "#"
    
    return jsonify({'frase': frase, 'gif_url': gif_url})

@main.route('/')
def home():
    return render_template('index.html')
