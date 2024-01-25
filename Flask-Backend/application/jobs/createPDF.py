import os
from datetime import datetime, date
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from application.data.models.users import Logs
from application.data.models.inventory import Category, Products
from application.data.models.offers import Offers
from ..utils import getCategorySale, getPopularProduct
from ..jobs.CreateGraph import pieChart

def create_pdf(file_path):
    month = datetime.now().strftime('%B')
    # Create a PDF document
    doc = SimpleDocTemplate(file_path, pagesize=A4)

    # Create a list to hold the content of the PDF
    elements = []

    # Add a header
    header_style = getSampleStyleSheet()["Heading1"]
    header_text = Paragraph(f"<b>Monthly Report - {month}</b>", header_style)
    elements.append(header_text)

    # Add some text
    text = "Category Sales Graph\n\n"
    text_paragraph = Paragraph(text, getSampleStyleSheet()["Heading2"])
    elements.append(text_paragraph)
    data = getCategorySale()
    image_path = pieChart(data)
    # Add an image
    img = Image(image_path, width=300, height=300)
    elements.append(img)

    text = "Store Manager and Admin Logs Table\n\n"
    text_paragraph = Paragraph(text, getSampleStyleSheet()["Heading2"])
    elements.append(text_paragraph)

    # Add a table
    data = [
        ['Table Name', 'Action', 'Name', 'User ID','Is Admin']
    ]
    logs = Logs.query.all()
    for l in logs:
        if datetime.strptime(l.date, "%Y-%m-%\d %H:%M:%S.%/f").date() == date.today():
            if l.table_name == 'category':
                c1 = Category.query.get(l.action_on)
                data.append(['Category',l.action,c1.c_name, l.user_id, bool(l.is_admin)])
            elif l.table_name == 'products':
                p1 = Products.query.get(l.action_on)
                data.append(['Category',l.action,p1.p_name, l.user_id, bool(l.is_admin)])
            else:
                o1 = Offers.query.get(l.action_on)
                data.append(['Category',l.action,o1.o_name, l.user_id, bool(l.is_admin)])

    table = Table(data, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    elements.append(table)

    text = "Top Popular Products\n\n"
    text_paragraph = Paragraph(text, getSampleStyleSheet()["Heading2"])
    elements.append(text_paragraph)
    popular = getPopularProduct()
    for p in popular:
        text = f"{p.p_name}\n\n"
        text_paragraph = Paragraph(text, getSampleStyleSheet()["BodyText"])
        elements.append(text_paragraph)

    # Build the PDF document
    doc.build(elements)
    count = len(os.listdir('./PDF_Report/'))
    output_file = f"./PDF_Report/pdf_{count}.pdf"
    create_pdf(output_file)
    print(f"PDF created successfully: {output_file}")

    return output_file
