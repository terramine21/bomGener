import openpyxl # для работы с exel
from fastapi import UploadFile, File
from typing import List, Dict
from tempfile import NamedTemporaryFile
import os

from schemas.schemas import DemoRecordCreate

async def parse_uploaded_bom(file: UploadFile) -> List[Dict]:
    """Парсит загруженный BOM-файл и возвращает данные"""
    with NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        return parse_altium_bom(temp_file_path)
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

# явно - возвращаем словарь
def parse_altium_bom(file_path: str) -> List[Dict]:
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    bom_data = []
    headers = [cell.value for cell in sheet[1]]  # Читаем первую строку первого листа
    col_index = {name: idx for idx, name in enumerate(headers) if name}

    for row in sheet.iter_rows(min_row=2, values_only=True): # хотим получить только значения ячеек
        try:
            item = {
                "designator": row[col_index["Designator"]] or "",
                "ad_bom": row[col_index["AD_BOM"]] or "",
                "ad_class": row[col_index["AD_CLASS"]] or "",
                "quantity": int(row[col_index["Quantity"]]) if row[col_index["Quantity"]] else 0,
                "ad_note": row[col_index["AD_NOTE"]] or "",
                "ad_ss": row[col_index["AD_SS"]] or ""
            }

            if item["designator"] is None or item["designator"] is "":  # если designator пуст
                continue  # пропускаем строку

            # используем DemoRecordCreate для валидации и конвертации данных
            record = DemoRecordCreate(**item)

            bom_data.append(dict(record)) # сохраняем как словарь
        except (IndexError, KeyError, ValueError) as e:
            print(f"Ошибка в строке {row}: {str(e)}")
            continue

    return bom_data

