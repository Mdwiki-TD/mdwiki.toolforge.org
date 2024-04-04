function to_get() {
	const ele = $("[hrefjson]");
	ele.each(function () {
		const item = $(this);
		let hrefjson = item.attr("hrefjson");
		// get the data from the hrefjson then add it to the value
		// ---
		const proxy = window.location.origin + '/ncc2/api/all.php?type=json&url=';
		// if localhost use proxy
		if (window.location.hostname === 'localhost') {
			hrefjson = proxy + encodeURIComponent(hrefjson);
		}
		// ---
		jQuery.ajax({
			url: hrefjson,
			// data: params,
			type: 'GET',
			success: function (data) {
				// ---
				console.log("to.js success:");
				console.log(hrefjson);
				// ---
				let view = 0;
				const items = data.items;
				// get view count from items array
				items.forEach(function (aa) {
					view += aa['views'];
					// console.log(view);
				});
				//---
				item.text(view);
				const pa = item.parent();
				pa.attr('data-sort', view);
				//---
				// var txt2 = $("<span></span>").text(view).hide();     // Create with jQuery
				// item.before(txt2);
				//---
				const p = $('#hrefjsontoadd').text();
				// add the view to hrefjsontoadd value
				let nu = parseFloat(p) + view;
				$('#hrefjsontoadd').text(nu);
				//---
			},
			error: function (data) {
				console.log("to.js error:");
				console.log(hrefjson);
			}
		});
		// ---
	});
}