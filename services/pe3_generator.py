from openpyxl import Workbook
from io import BytesIO
from openpyxl.styles import Font


def generate_pe3(bom_data: list) -> BytesIO:
    wb = Workbook()
    ws = wb.active
    ws.title = "Перечень элементов"

    # Настройка шрифта
    font = Font(name='Calibri', size=11)

    # Заголовки
    headers = ["Поз. обозначение", "Наименование", "Кол.", "Примечание"]
    ws.append(headers)

    # Стиль для заголовков
    for col in range(1, 5):
        ws.cell(row=1, column=col).font = Font(name='Calibri', bold=True)

    # Заполнение данных
    for idx, item in enumerate(bom_data, start=2):
        ws.append([
            f"{item.ad_class or ''}{idx - 1}",
            item.ad_bom or "",
            item.quantity or 0,
            item.designator or ""
        ])

    # Автоширина колонок
    for column in ws.columns:
        max_length = 0
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column[0].column_letter].width = adjusted_width

    # Сохранение в буфер
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer