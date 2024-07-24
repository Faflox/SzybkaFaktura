import tkinter as tk
import os
from tkcalendar import DateEntry
from datetime import datetime, timedelta, date
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def main():
    root.mainloop()

def restrain_sale_date(event=None):
    issue_date=issue_date_var.get_date()
    sale_date = sale_date_var.get_date()
    if sale_date < issue_date:
        sale_date_var.set_date(issue_date)
        
def set_sale_date_as_issue_date(event=None):
    issue_date = issue_date_var.get_date()
    sale_date_var.set_date(issue_date)

def calc_payment_due_date():
    issue_date = issue_date_var.get_date()
    payment_due_date = issue_date + timedelta(weeks=2)
    return payment_due_date

def submit_form():
    invoice_number = invoice_number_var.get()
    
    seller_data = {
        'seller_name': seller_name_var.get(),
        'seller_city': seller_city_var.get(),
        'seller_street': seller_street_var.get(),
        'seller_house_number': seller_house_nr_var.get(),
        'seller_phone_number': seller_phone_number_var.get()
    }
    
    customer_data = {
        'customer_name': customer_name_var.get(),
        'customer_city': customer_city_var.get(),
        'customer_street': customer_street_var.get(),
        'customer_house_number': customer_house_nr_var.get()
    }
    
    data = {
        'issue_date': issue_date_var.get_date(), 
        'sale_date': sale_date_var.get_date(),
        'payment_due': calc_payment_due_date(),
        'payment_method': payment_method_var.get(),
        'currency': currency_var.get(),
        'product_name': product_name_var.get(),
        'quantity': quantity_var.get(),
        'unit': unit_var.get(),
        'net_price': net_price_var.get(),
        'vat_rate': vat_rate_var.get()
    }
    
    print('Data passed correctly')
    create_pdf(invoice_number, seller_data, customer_data, data)
    
def create_pdf(invoice_number, seller_data, customer_data, data):
    directory = "invoices"
    if not os.path.exists(directory):
        os.makedirs(directory)

    pdf_file = f"{date.today().year}_{date.today().month}_{invoice_number}_inv_.pdf"
    file_path = os.path.join(directory, pdf_file)
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))
    styles.add(ParagraphStyle(name='Left', alignment=0))
    
    title = Paragraph(f"{invoice_number}/{date.today().month}/{date.today().year}", styles['Title'])
    elements.append(title)  
    elements.append(Spacer(1, 1 * cm))
    
    seller_info = [
        ["<b>Seller:</b>"],
        [f"{seller_data['seller_name']}"],
        [f"{seller_data['seller_street']} {seller_data['seller_house_number']}"],
        [f"{seller_data['seller_city']}"],
        [f"Phone: {seller_data['seller_phone_number']}"]
    ]
    customer_info = [
        ["<b>Customer:</b>"],
        [f"{customer_data['customer_name']}"],
        [f"{customer_data['customer_street']} {customer_data['customer_house_number']}"],
        [f"{customer_data['customer_city']}"]
    ]
    
    seller_info = [[Paragraph(cell, styles['Normal']) for cell in row] for row in seller_info]
    customer_info = [[Paragraph(cell, styles['Normal']) for cell in row] for row in customer_info]


    table_data = [
        seller_info,
        customer_info
    ]

    table = Table(table_data, colWidths=[3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 1 * cm))
    
    data_table = [
        ["Issue Date", data['issue_date'].strftime('%Y-%m-%d')],
        ["Sale Date", data['sale_date'].strftime('%Y-%m-%d')],
        ["Payment Due Date", data['payment_due'].strftime('%Y-%m-%d')],
        ["Payment Method", data['payment_method']],
        ["Currency", data['currency']],
        ["Product Name", data['product_name']],
        ["Quantity", data['quantity']],
        ["Unit", data['unit']],
        ["Net Price", data['net_price']],
        ["VAT Rate", data['vat_rate']]
    ]
    
    data_table = [[Paragraph(str(cell), styles['Normal']) for cell in row] for row in data_table]

    table = Table(data_table)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 2 * cm))
    
    total_price = float(data['net_price']) * (1 + float(data['vat_rate'].strip('%')) / 100)
    total_info = f"<b>Total Price (with VAT):</b> {total_price:.2f} {data['currency']}"
    elements.append(Paragraph(total_info, styles['Normal']))
    elements.append(Spacer(1, 4 * cm))
    
    signatures = [["Seller's signature", "", "", "Buyer's signature", ""]]
    table = Table(signatures, colWidths=[3.25 * cm, 4 * cm, 1.5 * cm, 3.25 * cm, 4 * cm])
    
    table.setStyle(TableStyle([
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LINEBELOW', (1, 0), (1, 0), 1, colors.black),
    ('LINEBELOW', (4, 0), (4, 0), 1, colors.black),
    ]))
    

    elements.append(table)
    doc.build(elements)
    print("File created")

   
#tkmain_____________________________________________________________________________
root = tk.Tk()
root.title("Fast Invoice Generator")

#vars
invoice_number_var = tk.IntVar()
#seller
seller_name_var = tk.StringVar()
seller_city_var = tk.StringVar()
seller_street_var = tk.StringVar()
seller_house_nr_var = tk.IntVar()
seller_phone_number_var = tk.IntVar()
#customer
customer_name_var = tk.StringVar()
customer_city_var = tk.StringVar()
customer_street_var = tk.StringVar()
customer_house_nr_var = tk.IntVar()
#
issue_date_var = DateEntry(root, width=16)
issue_date_var.bind("<<DateEntrySelected>>", set_sale_date_as_issue_date)
sale_date_var = DateEntry(root, width=16)
sale_date_var.bind("<<DateEntrySelected>>", restrain_sale_date)
payment_due_var = DateEntry(root)
payment_method_values = ["Cash", "Credit Card", "Installment Sale", "Check", "PayPal", "Prepayment", "Bill of Exchange"]
payment_method_var = tk.StringVar(value=payment_method_values[0])
currency_var = tk.StringVar()
product_name_var = tk.StringVar()
unit_values = ["pcs", "hr", "L", "km"]
unit_var = tk.StringVar(value=unit_values[0])
quantity_var = tk.StringVar()
net_price_var = tk.StringVar()
vat_values = ["3%", "5.5%", "8.5%", "10%", "12%", "12.5%", "14%", "15%", "17%"]
vat_rate_var = tk.StringVar(value=vat_values[0])



labels = [
    "Invoice Number",
    "Seller", "City", "Street", "House Number", "Phone Number", 
    "Customer Name", "City", "Street", "House Number",
    "Issue Date", "Sale Date",
    "Payment Method", "Currency",
    "Product Name", "Unit", "Quantity", "Net Price", "VAT rate"
]

variables = [
    invoice_number_var,
    seller_name_var, seller_city_var, seller_street_var, seller_house_nr_var, seller_phone_number_var,
    customer_name_var, customer_city_var, customer_street_var, customer_house_nr_var, 
    issue_date_var, sale_date_var,
    payment_method_var, currency_var,
    product_name_var, unit_var, quantity_var, net_price_var, vat_rate_var
]

variable_type = [
    "invoice_number_var", 
    "seller_name_var", "seller_city_var", "seller_street_var", "seller_house_nr_var", "seller_phone_number_var",
    "customer_name_var", "customer_city_var", "customer_street_var", "customer_house_nr_var",
    "issue_date_var", "sale_date_var",
    "payment_method_var", "currency_var",
    "product_name_var", "unit_type_var", "quantity_var", "net_price_var", "vat_rate_var"
]

assert len(labels) == len(variables) == len(variable_type) 


for i, (label, var_name, var) in enumerate(zip(labels, variable_type, variables)):
    tk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
    if isinstance(var, DateEntry):
        var.grid(row=i, column=1, pady=5)
    elif var_name == "payment_method_var":
        tk.OptionMenu(root, var, *payment_method_values).grid(row=i, column=1, pady=5)
    elif var_name == "unit_type_var":
        tk.OptionMenu(root, var, *unit_values).grid(row=i, column=1, pady=5)
    elif var_name == "vat_rate_var":
        tk.OptionMenu(root, vat_rate_var, *vat_values).grid(row=i, column=1, pady=5)
    else:
        tk.Entry(root, textvariable=var).grid(row=i, column=1, padx=10, pady=5)

tk.Button(root, text="Generate Invoice", command=submit_form).grid(row=len(labels) + 1, column=0, columnspan=2, pady=20)

if __name__ == "__main__":
    main()