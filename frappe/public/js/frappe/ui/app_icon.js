// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt


frappe.provide("frappe.ui")
frappe.ui.app_icon = {
	get_html: function(app, small, modules) {
		if(!modules) {
			modules = frappe.modules;
		}

		var module = modules[app]
		var icon = module.icon;
		var color = module.color;
		var iconType = icon.split(".").slice(-1)[0];
		if(iconType === "svg") {
			$.ajax({
				url: frappe.urllib.get_full_url(icon),
				dataType: "text",
				async: false,
				success: function(data) {
					icon = data;
				}
			})
			icon = '<object>'+ icon+'</object>';
		} 
		else if(iconType == "jpg" || iconType == "png"){
			icon = '<i class="octicon" title="' + module.label + '">' + '<img src="' + icon + '">' + '</i>';
		} else {
			icon = '<i class="'+ icon+'" title="' + module.label + '"></i>';
		}
		return '<div class="app-icon'+ (small ? " app-icon-small" : "")
			+'" style="background-color: '+ color +'" title="'+ module.label +'">'+icon+'</div>'
	}
}
