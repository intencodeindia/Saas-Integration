app_name = "saas_integration"
app_title = "Saas Integration"
app_publisher = "Intencode India Private Limited"
app_description = "This Application Is Developed To Get The Subscription Data Into Erpnext System"
app_email = "info@intencode.com"
app_license = "mit"

after_install = ["saas_integration.customization.customer_custom_field.create_customer_id_field"]
before_uninstall = ["saas_integration.customization.customer_custom_field.delete_customer_id_field"]


# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "saas_integration",
# 		"logo": "/assets/saas_integration/logo.png",
# 		"title": "Saas Integration",
# 		"route": "/saas_integration",
# 		"has_permission": "saas_integration.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/saas_integration/css/saas_integration.css"
# app_include_js = "/assets/saas_integration/js/saas_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/saas_integration/css/saas_integration.css"
# web_include_js = "/assets/saas_integration/js/saas_integration.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "saas_integration/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "saas_integration/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "saas_integration.utils.jinja_methods",
# 	"filters": "saas_integration.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "saas_integration.install.before_install"
# after_install = "saas_integration.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "saas_integration.uninstall.before_uninstall"
# after_uninstall = "saas_integration.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "saas_integration.utils.before_app_install"
# after_app_install = "saas_integration.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "saas_integration.utils.before_app_uninstall"
# after_app_uninstall = "saas_integration.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "saas_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }


# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"saas_integration.tasks.all"
# 	],
	"daily": [
		"saas_integration.automation.sales_invoice_auto.process_draft_sales_invoices"
	],
	"hourly": [
		"saas_integration.api.payment_entries.payment_entry_import"
	],
# 	"weekly": [
# 		"saas_integration.tasks.weekly"
# 	],
# 	"monthly": [
# 		"saas_integration.tasks.monthly"
# 	],
    "cron": {
        "*/1 * * * *": [  
            "saas_integration.api.customer_api.sync_customers_from_external_api"
        ],
        "*/5 * * * *": [
            "saas_integration.api.subscription.subscription_add"
        ]

    }
 }

# Testing
# -------

# before_tests = "saas_integration.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "saas_integration.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "saas_integration.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["saas_integration.utils.before_request"]
# after_request = ["saas_integration.utils.after_request"]

# Job Events
# ----------
# before_job = ["saas_integration.utils.before_job"]
# after_job = ["saas_integration.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"saas_integration.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

