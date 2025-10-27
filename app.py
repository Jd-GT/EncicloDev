from flask import Flask, render_template, request, jsonify
from trie import Trie
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
trie = Trie()

# Configurar Gemini
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("⚠️ ERROR: No se encontró GEMINI_API_KEY en el archivo .env")
    exit()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.0-flash')

def cargar_diccionario(archivo='diccionario.txt'):
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            palabras = f.read().splitlines()
            for palabra in palabras:
                if palabra.strip():
                    trie.insert(palabra.strip())
        print(f"✅ {len(palabras)} palabras cargadas exitosamente")
    except FileNotFoundError:
        print(f"⚠️ Archivo {archivo} no encontrado. Creando diccionario de ejemplo...")
        crear_diccionario_ejemplo()

def crear_diccionario_ejemplo():
    palabras_ejemplo = [
        'print', 'printf', 'private', 'process', 'program', 'python',
        'flask', 'function', 'for', 'file', 'open', 'class', 'def',
        'import', 'from', 'return', 'if', 'else', 'while', 'try',
        'except', 'finally', 'with', 'as', 'lambda', 'yield',
        'docker', 'docker-compose', 'dockerfile', 'git', 'git commit', 
        'git push', 'git pull', 'git branch', 'git merge', 'git checkout',
        'subnet', 'subnetmask', 'subnetting', 'tcp', 'udp', 'http', 
        'https', 'ssh', 'ftp', 'dns', 'dhcp', 'router', 'switch',
        'network', 'microservices', 'microservice', 'container',
        'kubernetes', 'jenkins', 'api', 'rest', 'json', 'xml',
        'html', 'css', 'javascript', 'node', 'react', 'vue',
        'angular', 'mongodb', 'postgresql', 'redis', 'sql',
        'database', 'algorithm', 'array', 'list', 'dict', 'tuple',
        'string', 'int', 'float', 'bool', 'hash', 'stack', 'queue',
        'tree', 'graph', 'sort', 'search', 'binary', 'recursive'
    ]
    
    with open('diccionario.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(palabras_ejemplo))
    
    for palabra in palabras_ejemplo:
        trie.insert(palabra)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    data = request.get_json()
    prefix = data.get('prefix', '')
    
    if len(prefix) < 1:
        return jsonify({'suggestions': []})
    
    suggestions = trie.search(prefix)
    return jsonify({'suggestions': suggestions})

@app.route('/select', methods=['POST'])
def select_word():
    data = request.get_json()
    word = data.get('word', '')
    trie.increment_counter(word)
    return jsonify({'status': 'ok'})

@app.route('/generate-description', methods=['POST'])
def generate_description():
    """Genera una descripción usando Gemini AI"""
    data = request.get_json()
    word = data.get('word', '')
    
    if not word:
        return jsonify({'status': 'error', 'error': 'No se proporcionó palabra'})
    
    try:
        prompt = f"""Explica de forma breve y clara qué es '{word}' en programación o informática.

Requisitos:
- Máximo 50 palabras
- Lenguaje simple y directo
- Si es un comando, incluye un ejemplo de uso
- Responde en español

Palabra: {word}"""
        
        response = model.generate_content(prompt)
        description = response.text.strip()
        
        return jsonify({
            'status': 'success',
            'word': word,
            'description': description,
            'generated_by': 'Google Gemini 1.5 Flash'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': f'Error de Gemini: {str(e)}'
        })

@app.route('/add', methods=['POST'])
def add_word():
    data = request.get_json()
    word = data.get('word', '')
    
    if word:
        trie.insert(word)
        with open('diccionario.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{word}')
        return jsonify({'status': 'ok', 'message': f'Palabra "{word}" agregada'})
    
    return jsonify({'status': 'error', 'message': 'Palabra vacía'})

@app.route('/stats')
def stats():
    top_words = trie.get_stats()
    return jsonify({'top_words': top_words})

if __name__ == '__main__':
    cargar_diccionario()
    print("🚀 Servidor Flask iniciado en http://127.0.0.1:5000")
    print("🤖 IA activada: Google Gemini 2.0 Flash")
    app.run(debug=True)
