import requests
import json

def generar_guia_json():
    url = "https://iptv-epg.org/files/epg-ar.xml"
    print("Descargando EPG...")
    
    # Descargamos el archivo como texto crudo
    response = requests.get(url)
    contenido = response.text
    
    guia_filtrada = []
    # IDs de canales que buscas
    canales_interes = ["ESPN.ar", "TyCSports.ar", "FoxSports.ar", "DSports.ar"]
    
    # Separamos el contenido en bloques de 'programme' manualmente
    bloques = contenido.split('<programme')
    
    for bloque in bloques:
        # Buscamos el canal y el título en cada bloque
        for canal_id in canales_interes:
            if f'channel="{canal_id}"' in bloque:
                # Extraemos el título (buscamos entre <title... y </title>)
                inicio_titulo = bloque.find('<title')
                if inicio_titulo != -1:
                    inicio_texto = bloque.find('>', inicio_titulo) + 1
                    fin_texto = bloque.find('</title>', inicio_texto)
                    titulo = bloque[inicio_texto:fin_texto]
                    
                    # Extraemos la hora (buscamos start="YYYYMMDDHHMMSS")
                    inicio_start = bloque.find('start="')
                    if inicio_start != -1:
                        hora_raw = bloque[inicio_start+7 : inicio_start+19] # Extraemos 12 dígitos
                        hora = f"{hora_raw[8:10]}:{hora_raw[10:12]}"
                        
                        guia_filtrada.append({
                            "canal": canal_id.replace(".ar", ""), 
                            "evento": titulo, 
                            "hora": hora
                        })
                break
        
        if len(guia_filtrada) >= 15: break

    # Guardamos el JSON
    with open('guia_deportes.json', 'w', encoding='utf-8') as f:
        json.dump(guia_filtrada, f, ensure_ascii=False, indent=4)
    print("¡Éxito! Archivo generado ignorando errores de formato.")

if __name__ == "__main__":
    generar_guia_json()
