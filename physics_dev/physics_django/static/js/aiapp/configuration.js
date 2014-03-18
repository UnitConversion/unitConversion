/*
 * Configuration file for setting global variables
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 * @created Mar 6, 2014
 */

// For accessing the REST service
var serviceurl = "http://localhost:8000";

//Version number
var version = "0.1";

// Write logs to console
var writeLogs = true;

// Active interlock status map
var aiStatusMap = {
	'editable': 0,
	'approved': 1,
	'active': 2,
	'backup': 3,
	'history': 4
};