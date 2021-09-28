$(document).ready(function () {
	// COntact Form handler
	var contactForm = $(".contact-form");
	var contactFormMethod = contactForm.attr("method");
	var contactFormEndPoint = contactForm.attr("action");
	var contactFormSubmitBtn = contactForm.find("[type='submit']");
	var contactFormSubmitBtnTxt = contactFormSubmitBtn.val();

	function displaySending(submitBtn, defaultText, doSomething) {
		if (doSomething)
		{
			console.log("displaying");
			submitBtn.addClass("disabled");
			submitBtn.html("<i class='fa fa-spin fa-spinner' ></i> Sending...");
		} else {
			submitBtn.removeClass("disabled");
			submitBtn.html(defaultText);
		}
	}

	contactForm.submit(function (event) {
		event.preventDefault();
		
		var contactFormSubmitBtn = contactForm.find("[type='submit']");
		var contactFormSubmitBtnTxt = contactFormSubmitBtn.text();
		
		var contactFormData = contactForm.serialize();
		thisForm = $(this);

		displaySending(contactFormSubmitBtn, "", true);
		$.ajax({
			type: contactFormMethod,
			url: contactFormEndPoint,
			data: contactFormData,
			success: function (data) {
				thisForm[0].reset();
				displaySending(contactFormSubmitBtn, contactFormSubmitBtnTxt, false);
				$.alert({
					title: "Success",
					content: "Thank You for submission.",
					theme: "modern",
				});
			},
			error: function (error) {
				console.log(error);
				errData = error.responseJSON;
				console.log(errData);
				displaySending(contactFormSubmitBtn, contactFormSubmitBtnTxt, false);

				$.each(errData, function (key, value) {
					keyValidation = thisForm.find("[name='" + key + "']").parent();
					appendValue =
						"<span><li class='text-danger mx-4'>" +
						value[0].message +
						"</li></span>";
					keyValidation.append(appendValue);
				});
				// $.alert({
				// 	title: "Oops!",
				// 	content: "An Error Occurred",
				// 	theme: "modern",
				// });
			},
		});
	});

	// Auto search
	var searchForm = $(".search-form");
	searchInput = searchForm.find("[name='q']");
	submitBtn = searchForm.find("[type='submit']");
	var typingTimer;
	var typingInterval = 700;
	searchInput.keyup(function (e) {
		typingTimer = setTimeout(performSearch, typingInterval);
	});
	searchInput.keydown(function (e) {
		clearTimeout(typingTimer);
	});
	function performSearch() {
		submitBtn.addClass("disabled");
		submitBtn.html("<i class='fa fa-spin fa-spinner' ></i> Searching");
		var query = searchInput.val();
		if (window.location.href.includes("search")) {
			window.location.href = "?q=" + query;
		} else {
			window.location.href = "search/?q=" + query;
		}
	}

	// Cart and Add Product
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
				if (data.cart_items > 0) {
					cart_count.text(data.cart_items);
				} else {
					cart_count.text("");
				}

				var currentPath = window.location.href;
				console.log(currentPath);
				if (currentPath.includes("cart")) {
					refreshCart();
				}
			},
			error: function (errorData) {
				$.alert({
					title: "Opps!!!!",
					content: "An Error Occurred!! please try again later",
					theme: "modern",
				});
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
				$.alert({
					title: "Opps!!!!",
					content: "An Error Occurred!! please try again later",
					theme: "modern",
				});
				console.log(error);
			},
		});
	}
});
