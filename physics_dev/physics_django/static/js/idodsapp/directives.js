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

/*
 * Directive for displaying a table with results
 */
app.directive('offline_data', function() {
	return {
		restrict: 'E',
		template : '\n\
			<tr>\n\
				<td ng-repeat="property in offline.retrieve_show">\n\
					<span ng-if="property == \'status\'">{{statusMap[offline[property]]}}</span>\n\
					<span ng-if="property != \"status\"">{{offline[property]}}</span>\n\
				</td>\n\
				<td>\n\
					<button onclick="toggleTableRows(this, \"offline_data\"")" class="btn btn-info">Show</button>\n\
				</td>\n\
			</tr>\n\
			<tr class="info offline_data" style="display: none;">\n\
				<td colspan="3">\n\
					<table class="table table-bordered">\n\
						<tr ng-repeat="property in offline.retrieve_hide">\n\
							<td>{{offline.display[property] | iff : offline.display[property] : property | firstLetterUppercase}}</td>\n\
							<td ng-if="property != \"script_name\"" && property != \"data_file_name\"">{{offline[property]}}</td>\n\
							<td ng-if="property == \"script_name\""><span ng-if="!offline.script">Script was not saved!</span><button ng-if="offline.script" class="btn btn-info" ng-click="downloadScript(offline)">Download script file</button></td>\n\
							<td ng-if="property == \"data_file_name\""><button ng-click="downloadRawData(offline)" class="btn btn-info">Download raw file</button></td>\n\
						</tr>\n\
					</table>\n\
				</td>\n\
			</tr>\n\
		',
		scope: {
			offline: '=offline'
		},
		link: function (scope, element, attrs) {
            l("attrs");
            l(attrs);

            scope.$watch('offline', function (newVal) {
                l('offline', newVal);
            });
        }
	};
});