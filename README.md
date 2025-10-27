#  EncicloDev

Sistema de autocompletado con estructura de datos Trie e IA generativa especializada en programación.

##  Características

-  Búsqueda eficiente con Trie (O(m))
-  Descripciones generadas por Google Gemini AI
-  Estadísticas de palabras más buscadas
-  Diccionario extensible
-  Interfaz moderna con paleta de colores tierra

##  Instalación

### 1. Clona el repositorio

git remote add origin https://github.com/Jd-GT/EncicloDev.git



### 2. Crea un entorno virtual

python -m venv venv

**En Windows:**
venv\Scripts\activate



**En macOS/Linux:**
source venv/bin/activate



### 3. Instala las dependencias

pip install -r requirements.txt



### 4. Configura tu API key de Gemini

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

GEMINI_API_KEY=tu-api-key-aqui


**Obtén tu API key gratis en:** https://aistudio.google.com/apikey

## 💻 Uso

### Ejecutar la aplicación

python app.py


Abre tu navegador en: `http://127.0.0.1:5000`
