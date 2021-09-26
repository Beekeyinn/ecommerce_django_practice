$(document).ready(function () {
	var cartForm = $(".form-product-ajax");
	cartForm.submit(function (event) {
		event.preventDefault();
		var thisForm = $(this);
		var actionEndPoint = thisForm.attr("action");
		var httpMethod = thisForm.attr("method");
		var formData = thisForm.serialize();
		$.ajax({
			type: httpMethod,
			url: actionEndPoint,
			data: formData,
			success: function (data) {
				var submitSpan = thisForm.find(".submit-span");
				if (data.added) {
					submitSpan.html(
						"<button type='submit' class=' btn btn-outline-danger'>Remove From Cart</button>"
					);
				} else {
					submitSpan.html(
						"<button type='submit' class='btn btn-outline-success' >Add To Cart</button>"
					);
				}
				var cart_count = $(".navbar-cart-count");
				if (data.cart_items > 0)
				{
					cart_count.text(data.cart_items);
				}else{
					cart_count.text("");
				}
				
				var currentPath = window.location.href;
				console.log(currentPath);
				if (currentPath.includes("cart")) {
					refreshCart();
				}
			},
			error: function (errorData) {
				console.error("ERROR: ", errorData);
			},
		});
	});

	function refreshCart() {
		console.log("contains cart");
		var cartTable = $(".cart-table");
		var cartBody = cartTable.find(".cart-body");
		// cartBody.html("<h1>Changed</h1>")
		var productRows = cartBody.find(".cart-product");
		var currentLocation = window.location.href;
		var refreshCartUrl = "api/cart/";
		var refreshCartMethod = "GET";
		var data = {};
		$.ajax({
			url: refreshCartUrl,
			data: data,
			method: refreshCartMethod,
			success: function (data) {
				var hiddenCartItemRemoveForm = $(".cart-product-remove-form");
				if (data.products.length > 0) {
					productRows.html(" ");
					i = data.products.length;

					$.each(data.products, function (index, prod) {
						var newRemoveForm = hiddenCartItemRemoveForm.clone();
						newRemoveForm.css("display", "block");
						newRemoveForm.find(".cart-item-product-id").val(prod.id);
						cartBody.prepend(
							'<tr><th scope="row">' +
								i +
								"</th><td><a href=" +
								prod.url +
								">" +
								prod.name +
								"</a>" +
								newRemoveForm.html() +
								"</td><td>" +
								prod.price +
								"</td></tr>"
						);
						i--;
					});

					cartBody.find(".cart-sub-total").text(data.subTotal);
					cartBody.find(".cart-total").text(data.total);
				} else {
					window.location.href = currentLocation;
				}
			},
			error: function (error) {
				console.log(error);
			},
		});
	}
});
