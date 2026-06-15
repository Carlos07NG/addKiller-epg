import ijson # Librería para leer archivos gigantes sin cargar todo en RAM
import json
import requests

def generar_guia_json():
    url = "https://iptv-epg.org/files/epg-ar.xml"
    
    # Abrimos la conexión como stream (sin descargar todo a RAM)
    r = requests.get(url, stream=True)
    
    guia_filtrada = []
    canales_interes = ["ESPN.ar", "TyCSports.ar", "FoxSports.ar"]
    
    # Usamos ijson para iterar el XML objeto por objeto
    # Nota: Como XMLTV es complejo, leeremos solo los tags 'programme'
    import xml.etree.ElementTree as ET
    
    context = ET.iterparse(r.raw, events=('end',))
    for event, elem in context:
        if elem.tag == 'programme':
            canal = elem.get('channel')
            if canal in canales_interes:
                titulo = elem.find('title').text if elem.find('title') is not None else "Sin título"
                hora_raw = elem.get('start', '00000000000000')
                hora = f"{hora_raw[8:10]}:{hora_raw[10:12]}"
                
                guia_filtrada.append({"canal": canal, "evento": titulo, "hora": hora})
                if len(guia_filtrada) >= 15: break
            
            # Limpiamos el elemento para liberar RAM
            elem.clear()
            
    with open('guia_deportes.json', 'w', encoding='utf-8') as f:
        json.dump(guia_filtrada, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generar_guia_json()
