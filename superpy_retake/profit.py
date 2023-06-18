# Imports
import csv
import os
from fpdf import FPDF

file_path_profit = os.path.abspath("profit.csv")

with open(file_path_profit, newline='') as f:
    reader = csv.reader(f)
    pdf = FPDF()
    pdf.add_page()
    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font('Arial', 'B', 14.0)
    pdf.cell(page_width, 0.0, 'Profit Data', align='C')
    pdf.ln(10)

    pdf.set_font('Courier', '', 10)

    col_width = page_width/7

    pdf.ln(1)

    th = pdf.font_size

    for row in reader:
        # print(row)
        pdf.cell(col_width, th, str(row[0]), border=1)
        pdf.cell(col_width, th, row[1], border=1)
        pdf.cell(col_width, th, row[2], border=1)
        pdf.cell(col_width, th, row[3], border=1)
        pdf.cell(col_width, th, row[4], border=1)
        pdf.cell(col_width, th, row[5], border=1)
        pdf.cell(col_width, th, row[6], border=1)
        pdf.ln(th)

    pdf.ln(10)

    pdf.output('profit.pdf', 'F')
