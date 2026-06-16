import requests
import gzip
import json
import io
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# Zona horaria Argentina
ARG_TZ = timezone(timedelta(hours=-3))


def generar_guia_json():
    url = "https://iptv-epg.org/files/epg-ar.xml.gz"

    print("Descargando EPG...")

    response = requests.get(url, timeout=180)
    response.raise_for_status()

    with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as gz:
        xml_content = gz.read()

    print("Procesando XML...")

    root = ET.fromstring(xml_content)

    programas = root.findall("programme")

    ahora_utc = datetime.now(timezone.utc)

    eventos_actuales = []

    for prog in programas:
        try:
            inicio = prog.get("start", "")
            fin = prog.get("stop", "")
            canal = prog.get("channel", "")

            if not inicio or not fin:
                continue

            dt_inicio = datetime.strptime(
                inicio[:14],
                "%Y%m%d%H%M%S"
            ).replace(tzinfo=timezone.utc)

            dt_fin = datetime.strptime(
                fin[:14],
                "%Y%m%d%H%M%S"
            ).replace(tzinfo=timezone.utc)

            # Solo programas en emisión ahora
            if not (dt_inicio <= ahora_utc <= dt_fin):
                continue

            title = prog.find("title")

            if title is None:
                continue

            titulo = (title.text or "").strip()

            # Convertir a hora Argentina
            dt_inicio_local = dt_inicio.astimezone(ARG_TZ)
            dt_fin_local = dt_fin.astimezone(ARG_TZ)

            # Calcular progreso
            duracion_total = (dt_fin - dt_inicio).total_seconds()

            progreso = 0

            if duracion_total > 0:
                progreso = int(
                    ((ahora_utc - dt_inicio).total_seconds()
                     / duracion_total) * 100
                )

            progreso = max(0, min(100, progreso))

            eventos_actuales.append({
                "canal": canal,
                "evento": titulo,
                "hora_inicio": dt_inicio_local.strftime("%H:%M"),
                "hora_fin": dt_fin_local.strftime("%H:%M"),
                "progreso": progreso
            })

        except Exception as e:
            print(f"Error: {e}")
            continue

    eventos_actuales.sort(key=lambda x: x["canal"].lower())

    with open(
        "guia_deportes.json",
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(
            eventos_actuales,
            archivo,
            ensure_ascii=False,
            indent=4
        )

    print(f"Programas en emisión encontrados: {len(eventos_actuales)}")


if __name__ == "__main__":
    generar_guia_json()
