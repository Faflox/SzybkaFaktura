import os
import pytest
from datetime import date
from project import (
    submit_form,
    restrain_sale_date,
    set_sale_date_as_issue_date,
    calc_payment_due_date,
    invoice_number_var,
    seller_name_var,
    seller_city_var,
    seller_street_var,
    seller_house_nr_var,
    seller_phone_number_var,
    customer_name_var,
    customer_city_var,
    customer_street_var,
    customer_house_nr_var,
    issue_date_var,
    sale_date_var,
    payment_due_var,
    payment_method_var,
    currency_var,
    product_name_var,
    unit_var,
    quantity_var,
    net_price_var,
    vat_rate_var,
)

def test_pdf_generation():
    invoice_number_var.set(1234)
    seller_name_var.set("John Doe")
    seller_city_var.set("New York")
    seller_street_var.set("5th Avenue")
    seller_house_nr_var.set(123)
    seller_phone_number_var.set(123456789)
    customer_name_var.set("Jan Kowalski")
    customer_city_var.set("Warsaw")
    customer_street_var.set("Wiejska")
    customer_house_nr_var.set(456)
    issue_date_var.set_date(date(2024, 7, 1))
    sale_date_var.set_date(date(2024, 7, 2))
    payment_due_var.set_date(date(2024, 7, 15))
    payment_method_var.set("Credit Card")
    currency_var.set("USD")
    product_name_var.set("English Lesson")
    unit_var.set("pcs")
    quantity_var.set("2")
    net_price_var.set("50.00")
    vat_rate_var.set("8.5%")

    submit_form()

    expected_filename = f"{date.today().year}_{date.today().month}_1234_inv_.pdf"
    assert os.path.exists(f"invoices/{expected_filename}"), "PDF file was not created"
    
    
def test_date_constraints():
    issue_date_var.set_date(date(2024, 7, 1))

    sale_date_var.set_date(date(2024, 6, 30))
    restrain_sale_date()
    
    assert sale_date_var.get_date() == date(2024, 7, 1), "Sale date was not adjusted correctly"

    issue_date_var.set_date(date(2024, 7, 5))
    set_sale_date_as_issue_date()
    assert sale_date_var.get_date() == date(2024, 7, 5), "Sale date was not updated correctly after issue date change"

def test_payment_due_date_calculation():
    issue_date_var.set_date(date(2024, 7, 1))
    expected_payment_due_date = date(2024, 7, 15)
    payment_due_date = calc_payment_due_date()
    
    assert payment_due_date == expected_payment_due_date, f"Payment due date calculation is incorrect. Expected {expected_payment_due_date}, got {payment_due_date}"
