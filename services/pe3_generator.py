from openpyxl import Workbook
from io import BytesIO


def generate_pe3(bom_data: list) -> BytesIO:
    wb = Workbook()
    ws = wb.active

    # Заголовки по ГОСТ
    ws.append(["Поз. обозначение", "Наименование", "Кол.", "Примечание"])

    # Заполнение данными
    for i, item in enumerate(bom_data, start=1):
        ws.append([
            f"{item.ad_class}{i}",
            item.ad_bom,
            item.quantity,
            item.designator
        ])

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer