/*
 * Configuration file for setting global variables
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

/**
 * Variables that can be and should be configured by user
 */

// For accessing the REST service
var serviceurl = "http://localhost:8000/id/device";

//Version number
var version = "0.1";

// Write logs to console
var writeLogs = true;

// Types of data we can browse/create/update/delete
var dataTypes = [
	{name:"vendor", value:"Vendor"}
];

// Vendor fixed properties
var vendorProps = [
	{
		"name": "id",
		"display": "Id",
		"save": false,
		"update": false
	},
	{
		"name": "name",
		"display": "Name",
		"save": true,
		"update": true,
		"mandatory": true
	},
	{
		"name": "description",
		"display": "Description",
		"save": true,
		"update": true
	}
];