/**
 * Created by vitalik on 12.02.17.
 */

jQuery(document).ready(function(){
	"use strict";

if($('.header-absolute').length){

	var stickyNavTop = 40;

	var stickyNav = function(){
			var scrollTop = $(window).scrollTop();
			if (scrollTop > stickyNavTop) {
				$('.header-absolute').addClass('sticky');
			} else {
				$('.header-absolute').removeClass('sticky');
			}
		};
		stickyNav();
		// and run it again every time you scroll
		$(window).scroll(function() {
			stickyNav();
		});
	}
})