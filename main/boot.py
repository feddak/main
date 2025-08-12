import frappe

def boot_session(bootinfo):
    """
    Add custom task status options to boot info
    """
    # Extended task status options
    custom_task_status = [
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
    
    bootinfo.custom_task_status = custom_task_status