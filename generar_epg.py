import requests
import json
import re

def generar_guia_json():
    url = "https://www.free-epg.de/api/epg?country=AR"
    print("Descargando EPG desde free-epg.de...")
    
    # 🎭 Aquí está el truco: Simulamos ser la app de IPTV "Tivimate"
    headers = {
        "User-Agent": "Tivimate/4.7.0",
        "Accept": "*/*"
    }
    
    try:
        # Hacemos la petición disfrazados
        response = requests.get(url, headers=headers, timeout=30)
        contenido = response.text
        
        if len(contenido) < 500:
            print("El servidor devolvió muy pocos datos. Podría seguir bloqueado.")
            return
            
        print(f"Descarga exitosa. Tamaño: {len(contenido)} caracteres.")
        
        # Desarmamos el XML separando cada programa en bloques
        bloques = contenido.split('<programme')
        todos_los_eventos = []
        
        for bloque in bloques[1:]:
            try:
                # Buscamos la hora, canal y título dentro del bloque
                start_match = re.search(r'start="([^"]+)"', bloque)
                channel_match = re.search(r'channel="([^"]+)"', bloque)
                title_match = re.search(r'<title[^>]*>(.*?)</title>', bloque, re.DOTALL)
                
                if start_match and channel_match and title_match:
                    start_raw = start_match.group(1)
                    canal = channel_match.group(1)
                    titulo = title_match.group(1)
                    
                    # Limpiamos textos extraños del XML
                    titulo_limpio = titulo.replace('<![CDATA[', '').replace(']]>', '').strip()
                    canal_corto = canal.split('.')[0].upper()
                    
                    # Transformamos el formato largo de hora (20240305140000) a algo legible (14:00)
                    hora = f"{start_raw[8:10]}:{start_raw[10:12]}" if len(start_raw) >= 12 else "--:--"
                        
                    todos_los_eventos.append({
                        "canal": canal_corto,
                        "evento": titulo_limpio,
                        "hora": hora
                    })
                    
                    # Límite para que tu app de Flutter cargue velozmente
                    if len(todos_los_eventos) >= 60:
                        break
            except Exception:
                continue

        with open('guia_deportes.json', 'w', encoding='utf-8') as f:
            json.dump(todos_los_eventos, f, ensure_ascii=False, indent=4)
            
        print(f"¡Éxito! Se guardaron {len(todos_los_eventos)} programas en tu JSON.")

    except Exception as e:
        print(f"Error en el proceso: {e}")

if __name__ == "__main__":
    generar_guia_json()
