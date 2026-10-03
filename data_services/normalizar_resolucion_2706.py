#!/usr/bin/env python3
"""Convierte los anexos técnicos de la Resolución 2706 de 2025 a JSONL.

No requiere dependencias externas: lee directamente la estructura XML de XLSX.
Uso:
    python3 data_services/normalizar_resolucion_2706.py RUTA_AL_XLSX

El archivo de salida se escribe junto a este script como
``resolucion_2706_2025.jsonl``.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET


SPREADSHEET_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
OUTPUT_PATH = Path(__file__).with_name("resolucion_2706_2025.jsonl")

# La hoja 3 es la fuente canónica del Anexo 2: conserva tildes, pero elimina
# puntos del código. Las hojas 2 y 4 son presentaciones equivalentes.
ANNEXES = (
    (3, 2, "Lista tabular de procedimientos", re.compile(r"^\d+$")),
    (5, 3, "Códigos especiales para reporte de población indígena", re.compile(r"^[A-Z0-9]+$")),
    (6, 4, "Códigos para reporte de otras prestaciones en salud", re.compile(r"^[A-Z0-9]+$")),
    (7, 5, "Códigos para reporte de intervenciones colectivas", re.compile(r"^I\d+$")),
    (8, 6, "Códigos para reporte de gestión en salud pública", re.compile(r"^A\d+$")),
    (9, 7, "Códigos para reporte de procedimientos e intervenciones sobre condiciones y medio ambiente de trabajo", re.compile(r"^T\d+$")),
)

NOTE_TYPES = {
    "incluye:": "incluye",
    "excluye:": "excluye",
    "simultáneo:": "simultaneo",
}


def compact(value: str) -> str:
    """Normaliza espacios sin alterar el texto oficial ni sus tildes."""
    return " ".join(value.split())


def search_text(value: str) -> str:
    """Representación estable para búsquedas que no distinguen tildes."""
    decomposed = unicodedata.normalize("NFD", compact(value))
    return "".join(char for char in decomposed if unicodedata.category(char) != "Mn").upper()


def column_name(cell_ref: str) -> str:
    return re.sub(r"\d+$", "", cell_ref)


def shared_strings(workbook: ZipFile) -> list[str]:
    root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
    return [
        "".join(node.text or "" for node in item.findall(f".//{SPREADSHEET_NS}t"))
        for item in root.findall(f"{SPREADSHEET_NS}si")
    ]


def cell_value(cell: ET.Element, strings: list[str]) -> str:
    cell_type = cell.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(f".//{SPREADSHEET_NS}t"))

    value = cell.find(f"{SPREADSHEET_NS}v")
    if value is None:
        return ""
    raw_value = value.text or ""
    return strings[int(raw_value)] if cell_type == "s" else raw_value


def worksheet_rows(workbook: ZipFile, sheet_number: int, strings: list[str]):
    root = ET.fromstring(workbook.read(f"xl/worksheets/sheet{sheet_number}.xml"))
    for row in root.findall(f".//{SPREADSHEET_NS}sheetData/{SPREADSHEET_NS}row"):
        cells = {
            column_name(cell.get("r", "")): compact(cell_value(cell, strings))
            for cell in row.findall(f"{SPREADSHEET_NS}c")
        }
        yield int(row.get("r", "0")), cells.get("A", ""), cells.get("B", "")


def dotted_annex_2_code(code: str) -> str:
    """Reconstruye la forma oficial con puntos desde la hoja canónica."""
    parts_by_length = {
        2: (code[:2],),
        3: (code[:2], code[2:3]),
        4: (code[:2], code[2:3], code[3:4]),
        6: (code[:2], code[2:3], code[3:4], code[4:6]),
    }
    dotted_code = ".".join(parts_by_length[len(code)])
    # Los códigos hoja del procedimiento (seis dígitos) no llevan punto final;
    # los niveles agrupadores sí lo llevan en la publicación oficial.
    return dotted_code if len(code) == 6 else dotted_code + "."


def parent_codes(records: list[dict]) -> None:
    """Asigna el prefijo codificado más largo presente en el mismo anexo."""
    codes_by_annex: dict[int, set[str]] = defaultdict(set)
    for record in records:
        codes_by_annex[record["anexo"]].add(record["codigo"])

    for record in records:
        code = record["codigo"]
        available_codes = codes_by_annex[record["anexo"]]
        record["codigo_padre"] = next(
            (code[:length] for length in range(len(code) - 1, 0, -1) if code[:length] in available_codes),
            None,
        )


def normalize(workbook_path: Path) -> list[dict]:
    records: list[dict] = []
    with ZipFile(workbook_path) as workbook:
        strings = shared_strings(workbook)
        for sheet_number, annex, annex_name, code_pattern in ANNEXES:
            latest_record: dict | None = None
            for row_number, raw_code, description in worksheet_rows(workbook, sheet_number, strings):
                note_type = NOTE_TYPES.get(raw_code.casefold())
                if note_type and latest_record is not None:
                    latest_record[note_type].append(description)
                    continue

                # Se excluyen títulos, encabezados y los rótulos de sección/capítulo.
                if not code_pattern.fullmatch(raw_code) or not description:
                    continue

                record = {
                    "codigo": raw_code,
                    "descripcion": description,
                    "descripcion_busqueda": search_text(description),
                    "anexo": annex,
                    "nombre_anexo": annex_name,
                    "incluye": [],
                    "excluye": [],
                    "simultaneo": [],
                    "fuente": {
                        "resolucion": "2706 de 2025",
                        "hoja": sheet_number,
                        "fila": row_number,
                    },
                }
                if annex == 2:
                    record["codigo_con_puntos"] = dotted_annex_2_code(raw_code)
                records.append(record)
                latest_record = record

    parent_codes(records)
    return records


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"Uso: {Path(sys.argv[0]).name} RUTA_AL_XLSX")

    records = normalize(Path(sys.argv[1]))
    with OUTPUT_PATH.open("w", encoding="utf-8") as output:
        for record in records:
            output.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"{len(records)} registros escritos en {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
