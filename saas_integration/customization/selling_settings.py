import frappe

def add_customer_id_option():

    selling_settings = frappe.get_doc("Selling Settings", "Selling Settings")
    
    
    existing_options = selling_settings.cust_master_name or ""
    
    
    if "Customer Id" not in existing_options:
        existing_options += "\nCustomer Id"  
    
    
    selling_settings.db_set("cust_master_name", existing_options)
    
    
    frappe.db.commit()

def remove_customer_id_option():
    
    selling_settings = frappe.get_doc("Selling Settings", "Selling Settings")
    
    
    existing_options = selling_settings.cust_master_name or ""
    
    
    if "Customer Id" in existing_options:
        updated_options = "\n".join([option for option in existing_options.split("\n") if option != "Customer Id"])
        selling_settings.db_set("cust_master_name", updated_options)
    
    
    frappe.db.commit()
