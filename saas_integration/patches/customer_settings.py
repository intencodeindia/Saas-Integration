import frappe

def add_customer_id_option():
    field = frappe.get_doc("DocField", {
        "parent": "Selling Settings",
        "fieldname": "cust_master_name"
    })

    if "Customer Id" not in field.options.split("\n"):
        new_options = field.options + "\nCustomer Id"
        field.options = new_options
        field.save()
        frappe.db.commit()

def remove_customer_id_option():
    field = frappe.get_doc("DocField", {
        "parent": "Selling Settings",
        "fieldname": "cust_master_name"
    })

    options = field.options.split("\n")
    if "Customer Id" in options:
        options.remove("Customer Id")
        field.options = "\n".join(options)
        field.save()
        frappe.db.commit()
