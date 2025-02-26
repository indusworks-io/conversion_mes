frappe.pages['manufacturing-order'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Manufacturing Order List',
		single_column: true
	});

	frappe.require('list.bundle.js', () => {
        let options = {
            doctype: 'Manufacturing Order',
            parent: page.body,
            show_sidebar: true, // To retain the sidebar in list view
        };
        new frappe.views.ListView(options);
    });
}