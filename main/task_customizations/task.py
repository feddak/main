import frappe
from frappe import _

# Extended task status options
CUSTOM_TASK_STATUS = [
    "Open",
    "Working", 
    "Ready to Test",
    "Testing",
    "Ready for Production",
    "Has a Problem",
    "Pending Review",
    "Overdue",
    "Completed",
    "Cancelled"
]

def extend_task_status_options(doc, method):
    """
    Extend the task status field options before validation
    """
    # Get the Task doctype
    task_meta = frappe.get_meta("Task")
    status_field = None
    
    # Find the status field
    for field in task_meta.fields:
        if field.fieldname == "status":
            status_field = field
            break
    
    if status_field:
        # Update the options for the status field
        status_field.options = "\n".join(CUSTOM_TASK_STATUS)

def validate_task_status(doc, method):
    """
    Validate that the task status is one of the allowed values
    """
    if doc.status and doc.status not in CUSTOM_TASK_STATUS:
        frappe.throw(
            _("Task status '{0}' is not valid. Allowed values are: {1}").format(
                doc.status, 
                ", ".join(CUSTOM_TASK_STATUS)
            ),
            title=_("Invalid Task Status")
        )
    
    # Custom business logic for different statuses
    if doc.status == "Ready to Test":
        # Ensure task is 100% complete before marking as ready to test
        if doc.progress < 100:
            frappe.msgprint(
                _("Task should be 100% complete before marking as 'Ready to Test'"),
                indicator="orange"
            )
    
    elif doc.status == "Testing":
        # You can add testing-related validations
        if not doc.assigned_to:
            frappe.msgprint(
                _("Please assign someone to test this task"),
                indicator="yellow"
            )
    
    elif doc.status == "Has a Problem":
        # Ensure there's a description of the problem
        if not doc.description or len(doc.description.strip()) < 10:
            frappe.throw(
                _("Please provide a detailed description of the problem in the task description"),
                title=_("Problem Description Required")
            )
    
    elif doc.status == "Ready for Production":
        # Ensure task has been tested
        if not doc.get("custom_tested_by") and not doc.get("custom_test_date"):
            frappe.msgprint(
                _("Please ensure the task has been properly tested before marking as 'Ready for Production'"),
                indicator="orange"
            )

def get_task_status_options():
    """
    Return the list of task status options
    """
    return CUSTOM_TASK_STATUS