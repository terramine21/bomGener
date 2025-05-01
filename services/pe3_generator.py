from openpyxl import Workbook


def generate_pe3(bom_data: List[Dict], output_path: str):
    wb = Workbook()
    ws = wb.active

    # Заголовки по ГОСТ
    ws.append(["Поз. обозначение", "Наименование", "Кол.", "Примечание"])

    # Группировка по типу компонента (AD_Class)
    grouped = {}
    for item in bom_data:
        key = item["ad_class"]
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(item)

    # Заполнение таблицы
    pos = 1
    for component_type, items in grouped.items():
        for item in items:
            ws.append([
                f"{component_type}{pos}",
                item["ad_bom"],
                item["quantity"],
                item["designator"]
            ])
            pos += 1

    wb.save(output_path)