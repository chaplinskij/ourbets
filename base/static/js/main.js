/**
 * Created by vitalik on 12.02.17.
 */


"use strict";
$(function () {
	let update_date_matches = function(date){
		var $date_matches = $('.date-matches');
		$.ajax({
			url: '/match/date/?date=' + date,
			success: function (data) {
				$date_matches.html(data);
				$('.change-date-match').on('click', function (e) {
					var $el = $(this);
					e.preventDefault();
					update_date_matches($el.data('date'));
				});
			}
		});
	};

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

   update_date_matches('20170407');

});