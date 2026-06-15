import requests
import xmltodict
import json

url_xml = "https://iptv-epg.org/files/epg-ar.xml"

def generar_guia_json():
    print("Descargando EPG gigante desde la nube...")
    response = requests.get(url_xml)
    
    print("Procesando datos...")
    data = xmltodict.parse(response.content)
    
    canales_interes = ["ESPN.ar", "TyCSports.ar", "FoxSports.ar", "ESPN2.ar", "DSports.ar"]
    guia_filtrada = []
    
    # Buscamos en el XML los canales que nos interesan
    for programa in data.get('tv', {}).get('programme', []):
        canal_id = programa.get('@channel', '')
        
        if canal_id in canales_interes:
            title_obj = programa.get('title', {})
            evento = title_obj.get('#text', title_obj) if isinstance(title_obj, dict) else title_obj
            
            hora_raw = programa.get('@start', '')
            if len(hora_raw) >= 12:
                hora_limpia = f"{hora_raw[8:10]}:{hora_raw[10:12]}"
            else:
                hora_limpia = "00:00"
                
            guia_filtrada.append({
                "canal": canal_id.replace(".ar", "").replace("Sports", " Sports"),
                "evento": evento,
                "hora": hora_limpia
            })
            
            # Solo guardamos los primeros 15 para que la app cargue al instante
            if len(guia_filtrada) >= 15:
                break

    # Creamos el archivo final
    with open('guia_deportes.json', 'w', encoding='utf-8') as f:
        json.dump(guia_filtrada, f, ensure_ascii=False, indent=4)
        
    print("¡JSON creado con éxito!")

generar_guia_json()
