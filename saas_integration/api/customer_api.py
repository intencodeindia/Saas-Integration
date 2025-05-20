import requests
import frappe
import json
from frappe import _, throw
from typing import Dict, Any


@frappe.whitelist()
def sync_customers_from_external_api() -> Dict[str, Any]:
    try:
        saas_api_settings = frappe.get_single("SaaS API Settings")

        url = saas_api_settings.customer_api_link
        auth_type = saas_api_settings.customer_auth_method       
        token = saas_api_settings.customer_api_pass_code         

        headers = _build_auth_headers(auth_type, token)

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        customers = _parse_api_response(response)
        results = _process_customers(customers)

        return {
            "status": "Success",
            "message": _("Customer import completed"),
            "details": results
        }

    except requests.exceptions.RequestException as e:
        return {"status": "Failed", "error": _("API request failed: {}").format(str(e))}

    except Exception as e:
        frappe.log_error(title="Customer Import Error", message=str(e))
        return {"status": "Failed", "error": _("Unexpected Error: {}").format(str(e))}


def _build_auth_headers(auth_type: str, token: str) -> Dict[str, str]:
    headers = {}
    if auth_type == "Bearer Token":
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _parse_api_response(response: requests.Response) -> list:
    try:
        data = response.json()

        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'data' in data:
            customers = data.get('data', [])
            if isinstance(customers, list):
                return customers
        raise ValueError(_("Invalid response format from API"))

    except json.JSONDecodeError:
        raise ValueError(_("Invalid JSON response from API"))


def _process_customers(customers: list) -> Dict[str, int]:
    results = {"total": len(customers), "created": 0, "failed": 0, "skipped": 0}

    for customer in customers:
        if not isinstance(customer, dict):
            results["failed"] += 1
            continue

        try:
            customer_name = customer.get("customer_id", "").strip()
            if not customer_name:
                results["failed"] += 1
                continue

            
            if frappe.db.exists("Customer", {"customer_name": customer_name}):
                results["skipped"] += 1
                continue

            customer_doc = _create_customer_doc(customer)
            customer_doc.insert(ignore_permissions=True)

            _create_customer_contact(customer, customer_doc.name)

            results["created"] += 1

        except Exception as e:
            results["failed"] += 1
            frappe.log_error(
                _("Customer Import Error"),
                f"{str(e)}\nPayload: {json.dumps(customer)}"
            )

    return results


def _create_customer_doc(customer: Dict[str, Any]) -> frappe.model.document.Document:
    return frappe.get_doc({
        "doctype": "Customer",
        "customer_name": customer.get("customer_id", "").strip(),  # Display name
        "customer_id": customer.get("customer_name", "").strip().lower(),  # Unique ID
        "customer_type": customer.get("customer_type", ""),
        "default_currency": customer.get("default_currency", "")
    })


def _create_customer_contact(customer: Dict[str, Any], customer_name: str):
    if not customer.get("email") and not customer.get("phone"):
        return

    contact = frappe.get_doc({
        "doctype": "Contact",
        "first_name": customer_name,
        "email_ids": [
            {
                "email_id": customer.get("email"),
                "is_primary": 1
            }
        ] if customer.get("email") else [],
        "phone_nos": [
            {
                "phone": customer.get("phone"),
                "is_primary_phone": 1
            }
        ] if customer.get("phone") else [],
        "links": [
            {
                "link_doctype": "Customer",
                "link_name": customer_name
            }
        ]
    })
    contact.insert(ignore_permissions=True)