import requests
import json
import re

def generar_guia_json():
    # Usamos la URL oficial y abierta de IPTV-org (Es 100% libre y responde siempre)
    url = "https://iptv-org.github.io/epg/guides/ar/mi.tv.xml"
    print("Descargando EPG desde servidor abierto...")
    
    # Agregamos un User-Agent para simular un navegador por las dudas
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        contenido = response.text
        print(f"Descargado correctamente. Tamaño del texto: {len(contenido)} caracteres.")
        
        # Buscamos los bloques de programas <programme ...> </programme>
        patron = re.compile(r'<programme\s+channel="([^"]+)".*?>.*?<title[^>]*>(.*?)</title>.*?start="([^"]+)"', re.DOTALL)
        matches = patron.findall(contenido)
        
        todos_los_eventos = []
        print(f"Se encontraron {len(matches)} coincidencias de programas crudos.")
        
        for match in matches:
            canal, titulo, start = match
            
            # Limpiamos el título por si viene con CDATA u otras etiquetas
            titulo_limpio = titulo.replace('<![CDATA[', '').replace(']]>', '').strip()
            
            # Formateamos la hora si tiene la longitud correcta (YYYYMMDDHHMMSS)
            if len(start) >= 12:
                hora = f"{start[8:10]}:{start[10:12]}"
            else:
                hora = "--:--"
            
            # Limpiamos el ID del canal para que quede lindo (ej: ESPN.ar -> ESPN)
            canal_corto = canal.split('.')[0].upper()
            
            todos_los_eventos.append({
                "canal": canal_corto,
                "evento": titulo_limpio,
                "hora": hora
            })
            
            # Guardamos los primeros 60 eventos para que la grilla de tu App esté bien completa
            if len(todos_los_eventos) >= 60:
                break

        # Guardamos el JSON
        with open('guia_deportes.json', 'w', encoding='utf-8') as f:
            json.dump(todos_los_eventos, f, ensure_ascii=False, indent=4)
            
        print(f"¡Éxito absoluto! guardados {len(todos_los_eventos)} canales en guia_deportes.json")

    except Exception as e:
        print(f"Error en la descarga o proceso: {e}")

if __name__ == "__main__":
    generar_guia_json()
