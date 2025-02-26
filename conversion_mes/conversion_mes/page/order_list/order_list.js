frappe.pages['order-list'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Manufacturing Order List',
        single_column: true
    });

	console.log(page);

	let field = page.add_field({
		label: 'Status',
		fieldtype: 'Select',
		fieldname: 'status',
		options: [
			'Open',
			'Closed',
			'Cancelled'
		],
		change() {
			console.log(field.get_value());
		}
	});	

    
};
