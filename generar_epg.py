import requests
import xmltodict
import json

def generar_guia_json():
    # URL directa del archivo en la web
    url = "https://iptv-epg.org/files/epg-ar.xml"
    print(f"Descargando desde {url}...")
    
    response = requests.get(url)
    data = xmltodict.parse(response.content)
    
    # IDs reales sacados de tu XML (ejemplos)
    canales_interes = ["ESPN.ar", "TyCSports.ar", "FoxSports.ar", "DSports.ar"]
    guia_filtrada = []
    
    for programa in data['tv']['programme']:
        canal_id = programa.get('@channel', '')
        if canal_id in canales_interes:
            # Extraemos info
            titulo = programa.get('title', 'Sin nombre')
            evento = titulo['#text'] if isinstance(titulo, dict) else titulo
            
            hora_raw = programa.get('@start', '00000000000000')
            hora_limpia = f"{hora_raw[8:10]}:{hora_raw[10:12]}"
            
            guia_filtrada.append({
                "canal": canal_id.replace(".ar", ""),
                "evento": evento,
                "hora": hora_limpia
            })
            
            if len(guia_filtrada) >= 10: break

    with open('guia_deportes.json', 'w', encoding='utf-8') as f:
        json.dump(guia_filtrada, f, ensure_ascii=False, indent=4)
    print("Éxito: Archivo generado.")

if __name__ == "__main__":
    generar_guia_json()
