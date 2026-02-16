import openpyxl
from openpyxl.styles import Font

class ExcelReport:
    def __init__(self, filename, headers):
        self.filename = filename
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active

        self.ws.append(headers)

        for cell in self.ws[1]:
            cell.font = Font(bold=True)

    def add_row(self, row):
        self.ws.append(row)

    def save(self):
        self.wb.save(self.filename)
