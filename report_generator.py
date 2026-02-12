import openpyxl

class ExcelReport:
    def __init__(self, filename, headers):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.append(headers)
        self.filename = filename

    def add_row(self, row):
        self.ws.append(row)

    def save(self):
        self.wb.save(self.filename)
        print(f"✅ Saved report: {self.filename}")
