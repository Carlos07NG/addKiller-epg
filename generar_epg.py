import requests
import gzip
import json
import re
import io

def generar_guia_json():
    url = "https://iptv-epg.org/files/epg-ar.xml.gz"
    print("Descargando EPG comprimido desde GitHub Actions...")
    
    headers = {"User-Agent": "Tivimate/4.7.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=60)
        # Corregido: se usa status_code en lugar de statusCode
        if response.status_code != 200:
            print(f"Error de servidor: {response.status_code}")
            return

        print("Descomprimiendo GZIP en la nube...")
        # Descomprimimos el archivo directamente en la memoria del servidor de GitHub
        with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
            xml_content = f.read().decode('utf-8')
        
        print("Procesando XML con Regex...")
        patron = re.compile(r'<programme\s+channel="([^"]+)".*?>.*?<title[^>]*>(.*?)</title>.*?start="([^"]+)"', re.DOTALL)
        matches = patron.findall(xml_content)
        
        todos_los_eventos = []
        print(f"Se encontraron {len(matches)} programas.")
        
        for match in matches:
            canal, titulo, start = match
            
            # Formateamos la hora de YYYYMMDDHHMMSS a HH:MM
            hora = f"{start[8:10]}:{start[10:12]}" if len(start) >= 12 else "--:--"
            titulo_limpio = titulo.replace('<![CDATA[', '').replace(']]>', '').strip()
            canal_corto = canal.split('.')[0].upper()
            
            todos_los_eventos.append({
                "canal": canal_corto,
                "evento": titulo_limpio,
                "hora": hora
            })
            
            # Dejamos un límite alto (ej: 1000) para tener casi todos los canales 
            # pero asegurando que la app siga abriendo de forma instantánea.
            if len(todos_los_eventos) >= 1000: 
                break

        # Guardamos el JSON final en el repositorio
        with open('guia_deportes.json', 'w', encoding='utf-8') as f:
            json.dump(todos_los_eventos, f, ensure_ascii=False, indent=4)
            
        print("¡JSON generado con éxito en el repositorio!")

    except Exception as e:
        print(f"Error en el proceso: {e}")

if __name__ == "__main__":
    generar_guia_json()
