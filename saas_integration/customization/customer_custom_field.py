import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_customer_id_field():
    custom_fields = {
        "Customer": [
            {
                "fieldname": "customer_id",
                "fieldtype": "Data",
                "label": "Customer Name",
                "insert_after": "customer_name",  
                "reqd": 1,  
                "in_list_view": 1,  
            }
        ]
    }

    for doctype, fields in custom_fields.items():
        for field in fields:
            
            if not frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}):
                create_custom_field(doctype, field)

def delete_customer_id_field():
    custom_fields_to_delete = {
        "Customer": ["customer_id"],  
    }

    for doctype, fields in custom_fields_to_delete.items():
        for field_name in fields:
            
            if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field_name}):
                frappe.delete_doc("Custom Field", f"{doctype}-{field_name}", ignore_missing=True)
                
    frappe.db.commit()  

   