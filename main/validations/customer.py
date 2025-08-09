import frappe
import re
from frappe import _

def validate_customer_name(doc, method):
    """
    Validate customer name to ensure it doesn't contain numbers
    
    Args:
        doc: The Customer document object
        method: The method that triggered this hook (e.g., 'validate')
    """
    
    # Check if customer_name field exists and has a value
    if not doc.customer_name:
        return
    
    # Check if the customer name contains any digits
    if re.search(r'\d', doc.customer_name):
        frappe.throw(
            _("Customer name '{0}' cannot contain numbers. Please use only letters and spaces.").format(doc.customer_name),
            title=_("Invalid Customer Name")
        )
    
    # Optional: Additional validations
    # Check for special characters (except spaces and common punctuation)
    if re.search(r'[^a-zA-Z\s\.\-\']', doc.customer_name):
        frappe.throw(
            _("Customer name can only contain letters, spaces, periods, hyphens, and apostrophes."),
            title=_("Invalid Customer Name")
        )
    
    # Optional: Check minimum length
    if len(doc.customer_name.strip()) < 2:
        frappe.throw(
            _("Customer name must be at least 2 characters long."),
            title=_("Invalid Customer Name")
        )

def before_save_customer(doc, method):
    """
    Additional processing before saving customer
    """
    # You can add more custom logic here
    # This runs before the validate method
    pass

def after_insert_customer(doc, method):
    """
    Actions to perform after customer is created
    """
    # This runs after the customer is successfully created
    # You can add logging, notifications, etc.
    frappe.logger().info(f"New customer created: {doc.customer_name}")