// Copyright 2007 Google Inc. All Rights Reserved.
//  ==========
//  gears_init
//  ==========
// Changed by: Alex(blackanger.z@gmail.com)
// Time : 2009.01.23


(function() {
	
	jQuery.fn.gearsInit = function(message_id){
		var check = false;

		if (window.google && google.gears) {
			check = true;
			return;
		}else{
			$(message_id).flashMessage("You must install Google Gears first.  <br/>  you can go <a href='http://gears.google.com'>here to DownLoad</>!");
			$(message_id).
			return;
		}

		
		if(check){
			var factory = null;

			// Firefox
			if (typeof GearsFactory != 'undefined') {

				factory = new GearsFactory();
			} else {
				// IE
				try {
					factory = new ActiveXObject('Gears.Factory');
				} catch (e) {
					// Safari
					if (navigator.mimeTypes["application/x-googlegears"]) {
						factory = document.createElement("object");
						factory.style.display = "none";
						factory.width = 0;
						factory.height = 0;
						factory.type = "application/x-googlegears";
						document.documentElement.appendChild(factory);
					}
				}
			}

			// *Do not* define any objects if Gears is not installed. This mimics the
			// behavior of Gears defining the objects in the future.
			if (!factory) {
				return;
			}

			// Now set up the objects, being careful not to overwrite anything.
			if (!window.google) {
				window.google = {};
			}

			if (!google.gears) {
				google.gears = {factory: factory};
			}
		}else{
			return false;
		}	
	};
	
})(jQuery);