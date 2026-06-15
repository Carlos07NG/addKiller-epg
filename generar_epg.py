import requests
import json
import re

def generar_guia_json():
    url = "https://iptv-epg.org/files/epg-ar.xml"
    print("Descargando todo el contenido...")
    
    response = requests.get(url)
    contenido = response.text
    
    # Expresión regular para capturar el canal, el título y la hora en cualquier orden
    # Buscamos bloques que empiecen con <programme y terminen en </programme>
    patron = re.compile(r'<programme\s+channel="([^"]+)".*?>.*?<title[^>]*>(.*?)</title>.*?start="([^"]+)"', re.DOTALL)
    
    todos_los_eventos = []
    
    # Encontramos todas las coincidencias en el texto
    matches = patron.findall(contenido)
    
    for match in matches:
        canal, titulo, start = match
        # Formateamos la hora: YYYYMMDDHHMMSS -> HH:MM
        hora = f"{start[8:10]}:{start[10:12]}"
        
        todos_los_eventos.append({
            "canal": canal,
            "evento": titulo,
            "hora": hora
        })
        
        # Limitamos a 50 eventos para no saturar el JSON y que la App cargue rápido
        if len(todos_los_eventos) >= 50:
            break

    with open('guia_deportes.json', 'w', encoding='utf-8') as f:
        json.dump(todos_los_eventos, f, ensure_ascii=False, indent=4)
    print(f"Éxito: Se procesaron {len(todos_los_eventos)} canales/eventos.")

if __name__ == "__main__":
    generar_guia_json()
