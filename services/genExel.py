CM_TO_POINTS = 28.35  # 1 см ≈ 28.35 точек

import openpyxl
from openpyxl.styles import Font
from datetime import datetime
from sqlmodel import select
from models.models import DemoRecord, Upload
from fastapi import HTTPException
from fastapi.responses import FileResponse
from tempfile import NamedTemporaryFile
from typing import List
import re


def group_designators(designators: str) -> str:
    if not designators.strip():  # если designator пуст, вернуть ""
        return ''

    # разбиваем строку на компоненты (designators)
    designators = sorted([d.strip() for d in designators.split(', ')])

    ranges = []  # для хранения диапазонов
    start_number = None
    prefix = ''

    for component in designators:
        new_prefix, number = component[0], int(component[1:])
        if start_number is not None and prefix == new_prefix and number - 1 == start_number + len(
                ranges) - 1:  # если можно продолжить группировку
            continue

        # сохранить диапазон в строковом формате
        if start_number is not None and len(ranges) > 0:
            ranges.append('{}{}-{}'.format(prefix, start_number, number - 1))

        # начинаем новую группу
        start_number = number
        prefix = new_prefix
        ranges = []  # сброс диапазона

    if start_number is not None:  # сохранить последний диапазон
        ranges.append('{}{}-{}'.format(prefix, start_number, number))

    return ', '.join(ranges)  # возвращаем все диапазона в строковом формате


def generate_excel_for_upload(upload_id: int, session):
    """
    Генерирует Excel файл для указанного upload_id и возвращает FileResponse
    """
    try:
        # Получаем записи
        records = session.exec(
            select(DemoRecord)
            .where(DemoRecord.upload_id == upload_id)
        ).all()

        if not records:
            raise HTTPException(status_code=404, detail="Записей нет")

        # Получаем информацию о загрузке
        upload = session.get(Upload, upload_id)
        if not upload:
            raise HTTPException(status_code=404, detail="Загрузка не найдена")

        # Создаем Excel табличку
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "BOM Data"
        default_font = Font(name='GOST Type A', size=14)
        wb._fonts = [default_font]

        # Заголовки
        headers = [
            "Поз. обозначение",
            "Наименование",
            "Кол.",
            "Примечание"
        ]
        ws.append(headers)

        column_widths = {
            'A': 2.0 * CM_TO_POINTS,    # 2.0 см
            'B': 11.0 * CM_TO_POINTS,   # 11.0 см
            'C': 1.0 * CM_TO_POINTS,    # 1.0 см
            'D': 4.5 * CM_TO_POINTS     # 4.5 см
        }
        for col_letter, width in column_widths.items():
            ws.column_dimensions[col_letter].width = width / 7


        # Данные
        for record in records:
            ws.append([
                group_designators(record.designator),
                f"{record.ad_class} {record.ad_bom} {record.ad_ss}".strip(),
                record.quantity,
                record.ad_note
            ])

        # Создаем временный файл (кросс-платформенный способ)
        with NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
            temp_file_path = temp_file.name
            wb.save(temp_file_path)

        # Генерируем имя файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bom_upload_{upload_id}_{timestamp}.xlsx"

        return FileResponse(
            path=temp_file_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при генерации Excel файла: {str(e)}"
        )
    finally:
        # Удаление временного файла будет выполнено FastAPI автоматически после отправки
        pass


