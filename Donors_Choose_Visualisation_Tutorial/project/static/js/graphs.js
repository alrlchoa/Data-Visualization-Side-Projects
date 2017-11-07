queue()
	.defer(d3.json, "/donorschoose/projects")
	.defer(d3.json, "static/geojson/us-states.json")
	.await(makeGraphs)

function makeGraphs(error, projectsJson, statesJson){
	var donorschooseprojects = projectsJson;
	var dateformat = d3.time.format("%Y-%m-%d %H:%M:%S");

	donorschooseprojects.forEach(function(d){
		d["date_posted"] = dateformat.parse(d["date_posted"]); //Parses date_posted to Y/M/D
		d["date_posted"].setDate(1); // Sets date to 1 to consolidate bins to months
		d["total_donations"] = +d["total_donations"]; // Makes otal_donations a number value
	});
	
	var ndx = crossfilter(donorschooseprojects); //Instantiate a Crossfilter
	
	//Defines Data Dimensions
	var dateDim = ndx.dimension(function(d){return d["date_posted"];});
	var resourceTypeDim = ndx.dimension(function(d){return d["resource_type"];});
	var povertyLevelDim = ndx.dimension(function(d){return d["poverty_level"];});
	var stateDim = ndx.dimension(function(d){return d["school_state"];});
	var totalDonationsDim = ndx.dimension(function(d){return d["total_donations"];});
	
	//Define Data groups for charts
	var all = ndx.groupAll();
	var numProjectsByDate = dateDim.group();
	var numProjectsByResourceType = resourceTypeDim.group();
	var numProjectsByPovertyLevel = povertyLevelDim.group();
	var totalDonationsByState = stateDim.group().reduceSum(function(d){return d["total_donations"];});
	var totalDonations = ndx.groupAll().reduceSum(function(d){return d["total_donations"];});
	
	//3 needed values. Will figure out what they do later. I think they are for normalizing the bar graphs
	var max_state = totalDonationsByState.top(1)[0].value;
	var minDate = dateDim.bottom(1)[0]["date_posted"]; 
	var maxDate = dateDim.top(1)[0]["date_posted"];
	
	//Making(Instantiating) the charts
	var timeChart = dc.barChart("#time-chart");
	var resourceTypeChart = dc.rowChart("#resource-type-row-chart");
	var povertyLevelChart = dc.rowChart("#poverty-level-row-chart");
	var usChart = dc.geoChoroplethChart("#us-chart");
	var numberProjectsND = dc.numberDisplay("#number-projects-nd");
	var totalDonationsND = dc.numberDisplay("#total-donations-nd");
	
	//Making Chart Parameters. Copied from tutorial because I am bad at making artistic choices.
	
	//Time Chart
	timeChart
	.width(600)
	.height(160)
	.margins({top: 10, right: 50, bottom: 30, left: 50})
	.dimension(dateDim)
	.group(numProjectsByDate)
	.transitionDuration(500)
	.x(d3.time.scale().domain([minDate, maxDate]))
	.elasticY(true)
	.xAxisLabel("Year")
	.yAxis().ticks(4);
	
	//Resource Type Chart
	resourceTypeChart
	.width(300)
	.height(250)
	.dimension(resourceTypeDim)
	.group(numProjectsByResourceType)
	.xAxis().ticks(4);
		
	//Poverty Level Chart
	povertyLevelChart
	.width(300)
	.height(250)
	.dimension(povertyLevelDim)
	.group(numProjectsByPovertyLevel)
	.xAxis().ticks(4);
	
	//US State Chart
	usChart
	.width(1000)
	.height(330)
	.dimension(stateDim)
	.group(totalDonationsByState)
	.colors(["#E2F2FF", "#C4E4FF", "#9ED2FF", "#81C5FF", "#6BBAFF", "#51AEFF", "#36A2FF", "#1E96FF", "#0089FF", "#0061B5"])
	.colorDomain([0, max_state])
	.overlayGeoJson(statesJson["features"], "state", function (d) {
		return d.properties.name;})
	.projection(d3.geo.albersUsa()
				.scale(600)
				.translate([340, 150]))
	.title(function (p) {
		return "State: " + p["key"]
				+ "\n"
				+ "Total Donations: " + Math.round(p["value"]) + " $";});
					
	//Number of Projects Number Display
	numberProjectsND
	.formatNumber(d3.format("d"))
	.valueAccessor(function(d){return d; })
	.group(all);
	
	//Total Donations Number Display
	totalDonationsND
	.formatNumber(d3.format("d"))
	.valueAccessor(function(d){return d; })
	.group(totalDonations)
	.formatNumber(d3.format(".3s"));
	
	dc.renderAll();
}