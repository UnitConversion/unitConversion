/*
 * Configuration file for setting global variables
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

/**
 * Variables that can be and should be configured by user
 */

// For accessing the REST service
var serviceurlraw = serviceurl;
var serviceurl = serviceurlraw + "id/device";

//Version number
var version = "0.1";

// Write logs to console
var writeLogs = true;

// Available groups of data types
var masterTypes = [
		{name: "device", value:"Device"},
		{name: "hierarchy", value:"Device hierarchy"},
		{name: "others", value: "Others"}
	];

// Types of data we can browse/create/update/delete
var dataTypes = {
	"device": [
		{name:"install", value:"Install"},
		{name:"inventory", value:"Inventory"}
	],
	"others": [
		{name:"vendor", value:"Vendor"},
		{name:"cmpnt_type", value:"Component type"},
		{name:"cmpnt_type_type", value:"Component type property type"},
		{name:"inventory_type", value:"Inventory property type"},
		{name:"inventory_to_install", value:"Inventory to Install"},
		{name:"install_rel", value:"Install relationship"},
		{name:"install_rel_type", value:"Install relationship property type"},
		{name:"data_method", value:"Data method"},
		{name:"offline_data", value:"Offline data"},
		{name:"offline_data_install", value:"Offline data (install)"},
		{name:"online_data", value:"Online data"},
		{name:"rot_coil_data", value:"Rot coil data"},
		{name:"hall_probe_data", value:"Hall probe data"}
	],
	"hierarchy": [
		{name:"beamline", value:"Beamline project"},
		{name:"installation", value:"Device geometric layout"}
	]};

// Map master types to data types
var mapMasterTypesToDataTypes = {
	"vendor": "others",
	"cmpnt_type": "others",
	"cmpnt_type_type": "others",
	"inventory_type": "others",
	"inventory_to_install": "others",
	"install_rel": "others",
	"install_rel_type": "others",
	"data_method": "others",
	"offline_data": "others",
	"offline_data_install": "others",
	"online_data": "others",
	"rot_coil_data": "others",
	"hall_probe_data": "others",

	"install": "device",
	"inventory": "device",

	"beamline": "hierarchy",
	"installation": "hierarchy"
};

// Define active/obsolete
var statusArr = [
	{name:1, value:"Active"},
	{name:0, value:"Obsolete"}
];

// Define status map
var statusArrMap = {
	1: statusArr[0].value,
	0: statusArr[1].value
};

// Node type options
var nodeTypeList = [
	{name:"root", value:"Root"},
	{name:"virtual", value:"Virtual"},
	{name:"real", value:"Real"}
];

// Device catagory options
var deviceCatagoryList = [
	{name:"id", value:"Insertion Device"},
	{name:"magnet", value:"Magnet"},
	{name:"other", value:"Other"}
];