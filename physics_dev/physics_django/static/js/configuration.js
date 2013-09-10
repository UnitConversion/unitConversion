/*
 * Configuration file for setting global variables
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

/**
 * Variables that can be and should be configured by user
 */

// For accessing the REST service
var serviceurl = "http://localhost:8000/";

//Version number
var version = "0.1";

//Write logs to console
var writeLogs = true;

//Current Log search url
var searchURL = "";

//How many logs do you want to load per request?
var numberOfLogsPerLoad = 20;

//Set the name of the cookie that holds selected filters
var filtersCookieName = "filters";

// Settings cookie name
var settingsCookieName = "converter";

//Selected filter elements are saved into an object
var selectedElements = {};

//Html file that contains templates
var templates = "../../static/html/templates.html";

// Html file that contain modal windows
var modalWindows = "static/html/modal_windows.html";

//Current Log displayed
var selectedLog = -1;

//Create object for saving device's details
var savedDevices = {};

// Selected filter elements are saved into an object
var selectedElements = {};

// Unit converter settings
var converterSettings = {};