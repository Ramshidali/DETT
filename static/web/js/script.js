// function resize() {

//   }
// $(document).ready(function () {
// 	$(".menuItems li").click(function () {
// 		$(this).addClass("active1").siblings().removeClass("active1");
// 	});
// 	$(".paginationContainer .pagination .circle").click(function () {
// 		$(this).addClass("active2").siblings().removeClass("active2");
// 	});
// 	$(document).on("scroll", onScroll);

// 	//smoothscroll
// 	$('a[href^="#"]').on("click", function (e) {
// 		e.preventDefault();
// 		$(document).off("scroll");

// 		if ($(this).hasClass("loginButton")) {
// 			console.log("--------------------log");
// 			$("#modalSection.loginModal").fadeIn();
// 			$("#modalSection .container .close").on("click", function () {
// 				$(".loginModal").fadeOut();
// 			});
// 		} else {
// 			$("a").each(function () {
// 				$(this).removeClass("active");
// 			});
// 			$(this).addClass("active");
// 		}

// 		var target = this.hash,
// 			menu = target;
// 		$target = $(target);
// 		if (target) {
// 			$("html, body")
// 				.stop()
// 				.animate(
// 					{
// 						scrollTop: $target.offset().top + 2,
// 					},
// 					500,
// 					"swing",
// 					function () {
// 						window.location.hash = target;
// 						$(document).on("scroll", onScroll);
// 					}
// 				);
// 		}
// 	});
// });

function onScroll(event) {
  var scrollPos = $(document).scrollTop();
  $("#spotlight header ul.nav li a").each(function () {
    var currLink = $(this);
    var refElement = $(currLink.attr("href"));
    var buisness = $("div#buisness");

    if (
      refElement.position().top <= scrollPos &&
      refElement.position().top + refElement.height() > scrollPos
    ) {
      $("#spotlight header ul.nav li a").removeClass("active");
      currLink.addClass("active");
    } else if (
      buisness.position().top + buisness.outerHeight(true) <=
      scrollPos
    ) {
      $("#spotlight header ul.nav li a.con").addClass("active");
      $("#spotlight header ul.nav li a.ab").addClass("active");
      $("#spotlight header ul.nav li a.serv").addClass("active");
    } else {
      currLink.removeClass("active");
    }
  });
}

$(document).ready(function () {
	$('#select-categories').on('click mousedown change', function(){
		$(".menuContainer .categories .angle_down").toggleClass("activate")
	});
    $('.itemContainer').on('click', function(){
		$(".menuContainer .angle_down").removeClass("activate")
	});

	})
  function equalcard(s) {
    var h = 0;
    var line_height = 0;
    $(s).css("display", "block").css("height", "auto");
    $(s).each(function () {
      var height = $(this).outerHeight(true);
      if (height > h) {
        h = height;
      }
    });
    $(s).height(h);
  }

  equalcard(".cardContainer .card .bottom .subtitle");
  $("#spotlight header .mobile").click(function () {
    $("#spotlight header .mobile").hide();
    $("#spotlight header .close").show();
    $("#spotlight .menu-container").slideDown("slow", function () {});
  });

  $("#spotlight header .close").click(function () {
    $("#spotlight header .close").hide();
    $("#spotlight header .mobile").show();
    $("#spotlight .menu-container").slideUp("slow", function () {});
  });

  $('a[href*="#"]:not([href="#"])').click(function (e) {
    e.preventDefault();
    $(document).off("scroll");
    $("#spotlight .menu ul li a.active").removeClass("active");
    $("#spotlight header ul.nav li a.active").removeClass("active");
    $("#spotlight header .close").hide();
    if ($(this).parents().hasClass("menu-container")) {
      $("#spotlight header .mobile").show();
    }
    $("#spotlight .menu-container").hide();
    $(this).addClass("active");

    var target = $(this.hash);
    target = target.length ? target : $("[name=" + this.hash.slice(1) + "]");
    if (target.length) {
      var height = $("#spotlight header").innerHeight();

      $("html,body").animate(
        {
          scrollTop: target.offset().top - height,
        },
        500
      );
      return false;
    }
  });

  var wow = new WOW({
    boxClass: "wow", // animated element css class (default is wow)
    animateClass: "animated", // animation css class (default is animated)
    offset: 0, // distance to the element when triggering the animation (default is 0)
    mobile: true, // trigger animations on mobile devices (default is true)
    live: true, // act on asynchronously loaded content (default is true)
    callback: function (box) {},
    scrollContainer: null, // optional scroll container selector, otherwise use window,
    resetAnimation: true, // reset animation on end (default is true)
  });
  wow.init();

  $(".slider-for").slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,

    asNavFor: ".slider-nav",
  });
  $(".slider-nav").slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    asNavFor: ".slider-for",
    dots: false,
    centerMode: false,
    focusOnSelect: true,
    vertical: true,
    responsive: [
      // {
      // 	breakpoint: 981,
      // 	settings: {
      // 		vertical: true,
      // 	},
      // },
      {
        breakpoint: 481,
        settings: {
          vertical: false,
        },
      },
    ],
  });

$(window).scroll(function () {
  var scroll_pos = 0;

  scroll_pos = $(this).scrollTop();

  if (scroll_pos > 0) {
    $("#spotlight header").css("background-color", "#fff");
    $("#spotlight header").css("box-shadow", "rgb(68 68 68 / 5%) 2px 3px 3px");
  } else if (scroll_pos == 0) {
    $("#spotlight header").removeAttr("style");
  }
});

// $("#customer_login").click(function () {
// 	$(".login-box").css({ display: "none" });
// 	$(".mobile-otp").css({ display: "block" });
// });

// $("#otp_validation").click(function () {
// 	$(".mobile-otp").css({ display: "none" });
// 	$("#myModal").css({ display: "none" });
// 	window.location.reload();
// });

// loginModalChange

$(".LoginOTP").hide();
$(".LoginPhone2").hide();
$(".LoginMain").hide();
$(".ForgotPassword").hide();
$(".PasswordReset").hide();

// $(".sb-btn-1").on("click", function () {
// 	$(".LoginPhone").hide();
// 	$(".LoginOTP").show();
// });
// $(".sb-btn-2").on("click", function () {
// 	$(".LoginOTP").hide();
// 	$(".LoginPhone2").show();
// });.loginButton
// $(".sb-btn-3").on("click", function () {
// 	$(".LoginPhone2").hide();
// 	$(".LoginMain").show();
// });
$(".forgot-Password").on("click", function () {
  $(".LoginMain").hide();
  $(".ForgotPassword").show();
});
$("#pro_forgot_pass").on("click", function () {
  $("#modalSection.password-reset").fadeOut();
  $(".LoginPhone").fadeOut();
  $("#modalSection.loginModal").fadeIn();
  $(".ForgotPassword").show();
});
// $(".sb-btn-5").on("click", function () {
// 	$(".ForgotPassword").hide();
// 	$(".LoginOTP").show();
// });

// modal close open
$(".jobOpening .wrapper .container .card .button").on("click", function () {
  pk = $(this).attr("data-pk");

  $("#career_application").find("*[name=designation]").val(pk);
  $(".modal").fadeIn();
});

$("#modalSection.modal .container .close").on("click", function () {
  $(".modal").fadeOut();
});

// successModal
$(".openSuccess").on("click", function () {
  $(".status-modal").fadeIn();
});
$(".closeSuccess").on("click", function () {
  $(".status-modal").fadeOut();
  window.location.reload();
});

// addresschange modal
// $(".addressChange_bt").on("click", function () {
// 	$(".address-change").fadeIn();
// });

// login modal close open
$("a.loginButton").on("click", function (e) {
  e.preventDefault();
  console.log("hiiiii");
  $(".loginModal").fadeIn();
});
$("#modalSection .container .close").on("click", function () {
  $(".loginModal").fadeOut();
});

// login modal open from signup modal
$(".loging-button-s1").click(function (e) {
  e.preventDefault();
  $(".signup-phone").hide();
  $(".login-phone").show();
});

// signup modal open from login modal
$(".signup-button-s2").click(function (e) {
  e.preventDefault();
  $(".login-phone").hide();
  $(".signup-phone").show();
});

// address modal close open
$(".address").on("click", function (e) {
  e.preventDefault();
  console.log("hiiiii");
  $(".addressModal").fadeIn();
});
$("#modalSection .container .close").on("click", function () {
  $(".addressModal").fadeOut();
});
