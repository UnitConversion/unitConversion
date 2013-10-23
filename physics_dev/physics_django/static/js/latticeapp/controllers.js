/*
 * Controllers for conversion module
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

app.controller('indexCtrl', function($scope, $location, $anchorScroll) {

	$scope.top = function() {
		l($location.hash());
		var id = $location.hash();

		// If no Log entry is selected, go to the top
		if(id === "" || id === "top") {
			$location.hash("top");
			$anchorScroll();

		// Scroll to the device
		} else {
			$location.hash("");
			var element = $('input[value=' + id + ']');
			l(element.offset().top);

			$('html, body').animate({
				scrollTop: element.parent().offset().top
			}, 100);
		}
	};
});

/*
 * Main controller when we load the main page
 */
app.controller('mainCtrl', function($scope){
	$scope.version = version;
	$scope.style = {};
	$scope.style.middle_class = "container-scroll-middle";
	$scope.style.right_class = "container-scroll-last-one";
	$scope.statuses = statuses;
});

/*
 * Controller for the left/search pane
 */
app.controller('searchFormCtrl', function($scope, systemService, $window, $routeParams){
	$scope.search = {};
	$scope.systems = [];
	$scope.search.displayLattice = "display_block";
	$scope.search.displayModel = "display_none";
	$scope.search.type = "lattice";
	$scope.search.selected = "-";

	// Set search type
	if($routeParams.type !== undefined) {
		$scope.search.type = $routeParams.type;
	}

	// Lattice search button click
	$scope.searchForLattice = function(search) {
		search.search = new Date().getTime();
		var newLocation = createDeviceListQuery(search, true) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};

	// Watch for search type change
	$scope.$watch('search.type', function(newValue, oldValue){

		if(newValue === "lattice") {
			$scope.search.displayLattice = "display_block";
			$scope.search.displayModel = "display_none";

		} else {
			$scope.search.displayLattice = "display_none";
			$scope.search.displayModel = "display_block";
		}
	});
});

/*
 * List devices in the middle pane
 */
app.controller('listLatticeCtrl', function($scope, $routeParams, $http, $window) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;

	$scope.lattices = [];
	var previousLattice = undefined;
	var query = "";

	query = serviceurl + 'lattice/?function=retrieveLatticeInfo&' + createDeviceListQuery($routeParams, false);
	l(query);

	$http.get(query).success(function(data){

		$.each(data, function(i, item){

			// Build customized Log object
			var newItem = item;

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.lattices.push(newItem);
		});
	});

	// Show details when user selects the lattice from a list
	$scope.showDetails = function(lattice){
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousLattice !== undefined) {
			previousLattice.click = "";
		}

		previousLattice = lattice;
		lattice.click = "lattice_click";
		lattice.search = $routeParams.search;
		lattice.type = $routeParams.type;

		var location = createDeviceListQuery(lattice, true) + "/details";
		l(location);

		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showDetailsCtrl', function($scope, $routeParams, $http, detailsService, $location, $sce){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.raw = {};
	$scope.raw.data = [];
	$scope.raw.show = true;
	$scope.lattices = [];
	$scope.lattice = {};

	var query = "";

	query = serviceurl + 'lattice/?function=retrieveLatticeInfo&' + createDeviceListQuery($routeParams, false);
	l(query);

	$http.get(query).success(function(data){
		$.each(data, function(i, item){

			$scope.lattices.push(item);
		});

		$scope.lattice = $scope.lattices[0];
		l($scope.lattices);
	});

	query = serviceurl + 'lattice/?function=retrieveLattice&withdata=true&' + createDeviceListQuery($routeParams, false);
	l(query);

	$http.get(query).success(function(data){
		//$('#raw').html(drawDataTree("", data));

		$.each(data, function(i, datum){
			var lattice = datum.lattice;
			var header = [];

			// Get the rest of the columns
			if(lattice.columns !== undefined) {
				header = lattice.columns;
			}
			l(header);

			$.each(lattice, function(i, line){
				
			});

			$scope.raw.data.push({head: header, body: lattice});
		});

		$scope.raw.show = false;
	});

	$scope.downloadFile = function() {

	};

	$scope.checkValue = function(column, line) {
		var string = "";

		if(line[column] !== undefined) {
			string = line[column][0];
		}

		if(string === undefined) {
			line[column][0] = $sce.trustAsHtml("");

		} else {

			if(column.indexOf("file") === -1) {
				line[column][0] = $sce.trustAsHtml(string);

			} else {
				var newString = string.replace(/"/g, '');
				line[column][0] = $sce.trustAsHtml("<a href='" + newString + "'>" + newString + "</a>");
			}
		}
	};

});

/*
 * Modal window example
 */
app.controller('modalCtrl', function($scope, $modalInstance) {
	$scope.ok = function() {
		$modalInstance.close();
	};

	$scope.cancel = function () {
		$modalInstance.dismiss('cancel');
	};
});