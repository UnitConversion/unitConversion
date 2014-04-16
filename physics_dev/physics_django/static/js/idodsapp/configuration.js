/*
 * Configuration file for setting global variables
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

/**
 * Variables that can be and should be configured by user
 */

// For accessing the REST service
var serviceurlraw = "http://localhost:8000/";
var serviceurl = serviceurlraw + "id/device";

//Version number
var version = "0.1";

// Write logs to console
var writeLogs = true;

// Types of data we can browse/create/update/delete
var dataTypes = [
	{name:"vendor", value:"Vendor"},
	{name:"cmpnt_type", value:"Component type"},
	{name:"cmpnt_type_type", value:"Component type property type"},
	{name:"inventory", value:"Inventory"},
	{name:"inventory_type", value:"Inventory property type"},
	{name:"install", value:"Install"},
	{name:"inventory_to_install", value:"Inventory to Install"},
	{name:"install_rel", value:"Install relationship"},
	{name:"install_rel_type", value:"Install relationship property type"},
	{name:"data_method", value:"Data method"},
	{name:"offline_data", value:"Offline data"},
	{name:"offline_data_install", value:"Offline data (install)"},
	{name:"online_data", value:"Online data"},
	{name:"beamline", value:"Beamline"},
	{name:"installation", value:"Installation"}
];