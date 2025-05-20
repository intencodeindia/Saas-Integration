# saas_integration.automation.sales_invoice_auto.process_draft_sales_invoices

import frappe
from frappe import _
from frappe.utils import get_url_to_form

def process_draft_sales_invoices():
    
    draft_invoices = frappe.get_all(
        "Sales Invoice",
        filters={"docstatus": 0},
        fields=["name", "customer", "outstanding_amount", "rounded_total"]
    )

    for invoice_info in draft_invoices:
        try:
            invoice = frappe.get_doc("Sales Invoice", invoice_info.name)

            
            invoice.allocate_advances_automatically = 1

            
            invoice.save(ignore_permissions=True)

            
            frappe.log_error(message=f"Invoice {invoice.name} saved with advances allocated. Outstanding amount: {invoice.outstanding_amount}", title="Invoice Allocation Status")

            
            if invoice.outstanding_amount <= 0.01:
                invoice.submit()  # Submit the invoice after clearing outstanding amount
                frappe.log_error(message=f"Invoice {invoice.name} has been submitted. Outstanding amount: {invoice.outstanding_amount}", title="Invoice Submission Status")
                send_sales_invoice_email(invoice)  # Send the email to the customer
            else:
                frappe.log_error(message=f"Invoice {invoice.name} not submitted. Outstanding amount: {invoice.outstanding_amount}", title="Invoice Submission Check")

        except Exception as e:
            frappe.log_error(message=str(e), title=f"Failed processing Sales Invoice {invoice_info.name}")


def send_sales_invoice_email(invoice):
    try:
        
        customer_email = get_customer_primary_email(invoice.customer)
        
        if not customer_email:
            frappe.log_error(message=f"No email found for customer: {invoice.customer}", title="Email Skipped")
            return

        
        subject = f"Invoice {invoice.name} from {invoice.company}"
        message = f"""
            <p>Dear Customer,</p>
            <p>Your invoice <strong>{invoice.name}</strong> is now available.</p>
            <p><a href="{get_url_to_form('Sales Invoice', invoice.name)}">View Invoice</a></p>
            <p>Thank you,<br>{invoice.company}</p>
        """

        
        frappe.sendmail(
            recipients=[customer_email],
            subject=subject,
            message=message,
            attachments=[frappe.attach_print("Sales Invoice", invoice.name)],  
            reference_doctype="Sales Invoice",
            reference_name=invoice.name
        )
        frappe.log_error(message=f"Email sent to {customer_email} for Invoice {invoice.name}", title="Email Sent Status")

    except Exception as e:
        frappe.log_error(message=str(e), title=f"Email sending failed for {invoice.name}")


def get_customer_primary_email(customer):
    """Returns the primary email of the customer contact."""
    result = frappe.db.sql("""
        SELECT ce.email_id
        FROM `tabContact` c
        JOIN `tabDynamic Link` dl ON dl.parent = c.name
        JOIN `tabContact Email` ce ON ce.parent = c.name
        WHERE dl.link_doctype = 'Customer'
          AND dl.link_name = %s
          AND ce.is_primary = 1
        LIMIT 1
    """, (customer,), as_dict=True)
    
    return result[0].email_id if result else None
