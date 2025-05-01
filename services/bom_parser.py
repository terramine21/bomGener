import openpyxl
from typing import List, Dict


def parse_altium_bom(file_path: str) -> List[Dict]:
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    bom_data = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        # Предполагаем структуру: Designator | AD_Class | AD_BOM | Quantity
        bom_data.append({
            "designator": row[0],
            "ad_class": row[1],
            "ad_bom": row[2],
            "quantity": row[3]
        })
    return bom_data