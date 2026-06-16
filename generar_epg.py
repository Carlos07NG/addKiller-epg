import requests
import gzip
import json
import io
import xml.etree.ElementTree as ET

def generar_guia_json():
    url = "https://iptv-epg.org/files/epg-ar.xml.gz"

    print("Descargando EPG comprimido desde GitHub Actions...")

    headers = {
        "User-Agent": "Tivimate/4.7.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=120
        )

        if response.status_code != 200:
            print(f"Error de servidor: {response.status_code}")
            return

        print("Descomprimiendo GZIP en memoria...")

        with gzip.GzipFile(
            fileobj=io.BytesIO(response.content)
        ) as gz:
            xml_content = gz.read()

        print("Parseando XML...")

        root = ET.fromstring(xml_content)

        programas = root.findall("programme")

        print(f"Programas encontrados en XML: {len(programas)}")

        todos_los_eventos = []

        for prog in programas:

            canal = prog.get("channel", "")

            inicio = prog.get("start", "")

            title = prog.find("title")

            if title is None:
                continue

            titulo = (title.text or "").strip()

            hora = "--:--"

            if len(inicio) >= 12:
                hora = f"{inicio[8:10]}:{inicio[10:12]}"

            canal_corto = canal.split(".")[0].upper()

            todos_los_eventos.append({
                "canal": canal_corto,
                "evento": titulo,
                "hora": hora
            })

            # límite para que el JSON no sea enorme
            if len(todos_los_eventos) >= 1000:
                break

        print(f"Se guardarán {len(todos_los_eventos)} eventos")

        with open(
            "guia_deportes.json",
            "w",
            encoding="utf-8"
        ) as archivo:
            json.dump(
                todos_los_eventos,
                archivo,
                ensure_ascii=False,
                indent=4
            )

        print("¡JSON generado con éxito!")

    except Exception as e:
        print(f"Error en el proceso: {e}")

if __name__ == "__main__":
    generar_guia_json()
