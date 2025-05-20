import requests
import frappe
import json
from frappe import _, throw
from typing import Dict, Any, List


@frappe.whitelist()
def payment_entry_import() -> Dict[str, Any]:
    try:
        settings = frappe.get_single("SaaS API Settings")

        url = settings.payment_api_link
        auth_type = settings.payment_auth_method
        token = settings.payment_api_pass_code

        
        paid_from_account = settings.payment_account_paid_from
        paid_to_account = settings.payment_account_paid_to

        if not paid_from_account or not paid_to_account:
            throw(_("Please configure both 'Payment Account Paid From' and 'Paid To' in SaaS API Settings."))

        headers = _build_auth_headers(auth_type, token)

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        payments = _parse_api_response(response)
        results = _process_payment_entries(payments, paid_from_account, paid_to_account)

        return {
            "status": "Success",
            "message": _("Payment Entry import completed"),
            "details": results
        }

    except requests.exceptions.RequestException as e:
        return {"status": "Failed", "error": _("API request failed: {}").format(str(e))}

    except Exception as e:
        frappe.log_error(title="Payment Entry Import Error", message=str(e))
        return {"status": "Failed", "error": _("Unexpected Error: {}").format(str(e))}


def _build_auth_headers(auth_type: str, token: str) -> Dict[str, str]:
    headers = {}
    if auth_type == "Bearer Token":
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _parse_api_response(response: requests.Response) -> List[Dict[str, Any]]:
    try:
        data = response.json()
        if isinstance(data, dict) and data.get("success") and isinstance(data.get("data"), list):
            return data["data"]
        raise ValueError(_("Invalid response format from API"))
    except json.JSONDecodeError:
        raise ValueError(_("Invalid JSON response from API"))


def _process_payment_entries(
    payments: List[Dict[str, Any]],
    paid_from_account: str,
    paid_to_account: str
) -> Dict[str, int]:
    results = {"total": len(payments), "created": 0, "failed": 0, "skipped": 0}

    for payment in payments:
        try:
            if payment.get("payment_order_status") != "PAYMENT_SUCCESS":
                results["skipped"] += 1
                continue

            if _payment_entry_exists(payment.get("cheque_reference_no")):
                results["skipped"] += 1
                continue

            payment_doc = _create_payment_entry_doc(payment, paid_from_account, paid_to_account)
            payment_doc.insert(ignore_permissions=True)
            payment_doc.submit()

            results["created"] += 1

        except Exception as e:
            results["failed"] += 1
            frappe.log_error(
                _("Payment Entry Import Error"),
                f"{str(e)}\nPayload: {json.dumps(payment)}"
            )

    return results


def _payment_entry_exists(cheque_reference_no: str) -> bool:
    return frappe.db.exists("Payment Entry", {"reference_no": cheque_reference_no})

def _create_payment_entry_doc(
    payment: Dict[str, Any],
    paid_from_account: str,
    paid_to_account: str
) -> frappe.model.document.Document:
    posting_date = "2024-01-01"

    return frappe.get_doc({
        "doctype": "Payment Entry",
        "payment_type": payment.get("payment_type"),
        "posting_date": posting_date,  
        "mode_of_payment": payment.get("mode_of_payment"),
        "party_type": payment.get("party_type"),
        "party": payment.get("party"),
        "party_name": payment.get("party_name"),
        "paid_from": paid_from_account,
        "paid_to": paid_to_account,
        "paid_amount": float(payment.get("paid_amount", 0)),
        "received_amount": float(payment.get("received_amount", 0)),
        "source_exchange_rate": 1.0,
        "target_exchange_rate": 1.0,
        "reference_no": payment.get("cheque_reference_no"),
        "reference_date": payment.get("cheque_reference_date") or frappe.utils.nowdate(),
    })

