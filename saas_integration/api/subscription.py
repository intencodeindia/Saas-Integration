import requests
import frappe
import json
from frappe import _, throw
from typing import Dict, Any, List


@frappe.whitelist()
def subscription_add() -> Dict[str, Any]:
    try:
        saas_api_settings = frappe.get_single("SaaS API Settings")

        url = saas_api_settings.subscription_api_link
        auth_type = saas_api_settings.subscription_auth_method
        token = saas_api_settings.subscription_api_pass_code

        headers = _build_auth_headers(auth_type, token)

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        subscriptions = _parse_api_response(response)
        results = _process_subscriptions(subscriptions)

        return {
            "status": "Success",
            "message": _("Subscription import completed"),
            "details": results
        }

    except requests.exceptions.RequestException as e:
        return {"status": "Failed", "error": _("API request failed: {}").format(str(e))}

    except Exception as e:
        frappe.log_error(title="Subscription Import Error", message=str(e))
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


def _process_subscriptions(subscriptions: List[Dict[str, Any]]) -> Dict[str, int]:
    results = {"total": len(subscriptions), "created": 0, "failed": 0, "skipped": 0}

    for sub in subscriptions:
        try:
            customer_id = sub.get("customer_id", "").strip()
            plan_name = sub.get("plan_name", "").strip()

            if not customer_id or not plan_name:
                results["failed"] += 1
                continue

            
            if _subscription_exists(customer_id, sub.get("customer_type", "Customer"), plan_name):
                results["skipped"] += 1
                continue

            sub_doc = _create_subscription_doc(sub)
            sub_doc.insert(ignore_permissions=True)

            results["created"] += 1

        except Exception as e:
            results["failed"] += 1
            frappe.log_error(
                _("Subscription Import Error"),
                f"{str(e)}\nPayload: {json.dumps(sub)}"
            )

    return results


def _subscription_exists(customer_id: str, customer_type: str, plan_name: str) -> bool:
    result = frappe.db.sql("""
        SELECT s.name
        FROM `tabSubscription` s
        JOIN `tabSubscription Plan Detail` p ON p.parent = s.name
        WHERE s.party = %s AND s.party_type = %s AND p.plan = %s
        LIMIT 1
    """, (customer_id, customer_type, plan_name), as_dict=True)
    return bool(result)


def _create_subscription_doc(subscription: Dict[str, Any]) -> frappe.model.document.Document:
    return frappe.get_doc({
        "doctype": "Subscription",
        "party_type": subscription.get("customer_type", "Customer"),
        "party": subscription.get("customer_id", "").strip(),
        "start_date": subscription.get("start_date", ""),
        "end_date": subscription.get("end_date", ""),
        "trial_period_start": subscription.get("trial_start_date", ""),
        "trial_period_end": subscription.get("trial_end_date", ""),
        "submit_invoice": 0,
        "generate_invoice_at": "Beginning of the current subscription period",
        "plans": [
            {
                "plan": subscription.get("plan_name", "").strip(),
                "qty": 1  
            }
        ]
    })
