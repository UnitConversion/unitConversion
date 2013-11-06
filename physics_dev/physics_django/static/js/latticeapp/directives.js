/*
 * This file contains angular.js directives
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

/*
 * Enter keypress event. It is primarily made for pressing enter on input tags
 */
app.directive('ngEnter', function() {
	return function(scope, element, attrs) {
		element.bind("keydown keypress", function(event) {

			if(event.which === 13) {
				scope.$apply(function(){
					scope.$eval(attrs.ngEnter);
				});

				event.preventDefault();
			}
		});
	};
});

/*
 * Compile HTML with angular directives
 */
app.directive('compile', function($compile) {
	return function(scope, element, attrs) {
		scope.$watch(
			function(scope) {
				return scope.$eval(attrs.compile);
			},
			function(value) {
				element.html(value);
				$compile(element.contents())(scope);
			}
		);
	};
});

/*
 * Resize bar between left and middle pane
 */
app.directive('resizeLeft', function() {
	return function(scope, element, attrs) {
		var leftPane = angular.element(".container-left");
		var middlePane = angular.element(".container-middle");
		var minWidth = 200;

		// Resize left and middle section
		$('.container-resize').draggable({axis: "x"});

		$('.container-resize').on('drag', function(e){
			var oldWidth = $(leftPane).width();
			var oldMiddleWidth = $(middlePane).width();
			var pageX = e.pageX;

			// Limit the minimal width of the left pane
			if(oldWidth < minWidth && pageX < oldWidth) {
				return;
			}

			// Limit the minimal width of the middle pane
			if(oldMiddleWidth < minWidth && pageX > oldMiddleWidth) {
				return;
			}

			var diff = oldWidth - pageX;
			$(leftPane).width(pageX);
			$(middlePane).css({left: pageX});
			$(middlePane).width($(middlePane).width() + diff);
		});

		// Stop dragging left resizer
		$('.container-resize').on('dragstop', function(e){
			$('.container-resize').css({left: $(leftPane).width()});
		});
	};
});

/*
 * Resize bar between left and middle pane
 */
app.directive('resizeRight', function() {
	return function(scope, element, attrs) {
		var leftPane = angular.element(".container-left");
		var middlePane = angular.element(".container-middle");
		var rightPane = angular.element(".container-right");
		var minWidth = 200;

		// Resize left and middle section
		$('.container-resize2').draggable({axis: "x"});

		$('.container-resize2').on('drag', function(e){
			var oldWidth = $(leftPane).width();
			var oldMiddleWidth = $(middlePane).width();
			var oldRightWidth = $(rightPane).width();
			var pageX = e.pageX - oldWidth;

			// Limit the minimal width of the middle pane
			if(oldMiddleWidth < minWidth && pageX < oldMiddleWidth) {
				return;
			}

			// Limit the minimal width of the right pane
			if(oldRightWidth < minWidth && pageX > oldRightWidth) {
				return;
			}

			$(middlePane).width(pageX);
			$(rightPane).css({left: e.pageX});
			$(rightPane).width($(window).width() - e.pageX);
		});

		// Stop dragging left resizer
		$('.container-resize2').on('dragstop', function(e){
			$('.container-resize2').css({left: $(leftPane).width() + $(middlePane).width()});
		});
	};
});