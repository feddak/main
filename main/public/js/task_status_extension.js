// Extend Task form with custom status options
frappe.ui.form.on('Task', {
    onload: function(frm) {
        // Update status field options
        if (frm.doc.doctype === 'Task') {
            const custom_status_options = [
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
            ].join('\n');
            
            // Update the field options
            frm.set_df_property('status', 'options', custom_status_options);
        }
    },
    
    status: function(frm) {
        // Custom logic when status changes
        if (frm.doc.status === 'Ready to Test') {
            frappe.msgprint(__('Task is ready for testing. Please assign a tester.'));
            frm.set_value('priority', 'High');
        }
        
        else if (frm.doc.status === 'Testing') {
            frappe.msgprint(__('Task is now being tested.'));
        }
        
        else if (frm.doc.status === 'Has a Problem') {
            frappe.msgprint({
                title: __('Problem Reported'),
                message: __('Please describe the problem in the task description.'),
                indicator: 'red'
            });
            
            // Set priority to high for problem tasks
            frm.set_value('priority', 'High');
        }
        
        else if (frm.doc.status === 'Ready for Production') {
            frappe.msgprint({
                title: __('Ready for Production'),
                message: __('Task has been tested and is ready for production deployment.'),
                indicator: 'green'
            });
        }
    }
});

// Extend Task List view
frappe.listview_settings['Task'] = {
    add_fields: ["status", "priority", "progress"],
    get_indicator: function(doc) {
        const status_colors = {
            "Open": "grey",
            "Working": "orange", 
            "Ready to Test": "blue",
            "Testing": "purple",
            "Ready for Production": "green",
            "Has a Problem": "red",
            "Pending Review": "yellow",
            "Overdue": "darkgrey",
            "Completed": "green",
            "Cancelled": "dark grey"
        };
        
        return [__(doc.status), status_colors[doc.status] || "grey", "status,=," + doc.status];
    }
};