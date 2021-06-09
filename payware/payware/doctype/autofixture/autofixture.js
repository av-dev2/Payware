// Copyright (c) 2021, Aakvatech and contributors
// For license information, please see license.txt

frappe.ui.form.on('AutoFixture', {
	//refresh: function(frm) {
	//frm.trigger()
	//}
});

frappe.ui.form.on("AutoFixture", "onload", function (frm) {
	frm.refresh();
});


frappe.ui.form.on('AutoFixture', {
	on_reload: function (frm) {
		frm.set_value('name', frm.doc.filter);
		frm.refresh_field('name');
	}
});