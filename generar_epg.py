import requests
import xmltodict
import json
import sys

def generar_guia_json():
    try:
        url = "https://iptv-epg.org/files/epg-ar.xml"
        print(f"Intentando descargar {url}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status() # Esto lanza error si la descarga falla
        
        print("Parseando XML...")
        data = xmltodict.parse(response.content)
        
        # Filtro de prueba simple para ver si encuentra algo
        canales_interes = ["ESPN.ar", "TyCSports.ar"]
        guia_filtrada = []
        
        programas = data.get('tv', {}).get('programme', [])
        print(f"Se encontraron {len(programas)} programas en el XML.")
        
        for programa in programas:
            if programa.get('@channel') in canales_interes:
                guia_filtrada.append({"evento": "prueba"})
        
        print(f"Objetos filtrados: {len(guia_filtrada)}")

        with open('guia_deportes.json', 'w', encoding='utf-8') as f:
            json.dump(guia_filtrada, f, ensure_ascii=False, indent=4)
        print("Archivo guardado con éxito.")
        
    except Exception as e:
        print(f"¡ERROR DETECTADO!: {str(e)}")
        sys.exit(1) # Esto le dice a GitHub que el proceso falló con razón

if __name__ == "__main__":
    generar_guia_json()
