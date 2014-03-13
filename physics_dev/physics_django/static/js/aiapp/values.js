/*
 * Values for active interlock
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 * @created: Mar 7, 2014
 */

/*
 * Logic object
 */
app.value('Logic', function(obj) {
	// Mandatory parameters for saving
	this.save_m = ["name"];

	// Parameters for saving
	this.save = ["name", "shape", "logic", "code"];
	
	// Mandatory parameters for retrieving
	this.retrieve_m = ["name"];
	
	// All parameters for retrieving
	this.retrieve = ["name", "shape", "logic", "code"];
	
	this.all = ["id", "name", "shape", "logic", "code"];

	this.id = "";
	this.name = "";
	this.shape = "";
	this.logic = "";
	this.code = "";

	this.set = function(obj) {

		if(obj === undefined) {
 			return undefined;
 		}

 		for(i=0; i<this.all.length; i++) {
 			this[this.all[i]] = obj[this.all[i]];
 		}
	}

	if(obj !== undefined) {
 		this.set(obj);
 	}
});

/*
 * Bending magnet object
 */
app.value('BendingMagnet', function(obj) {
	// Mandatory parameters for saving
	this.save_m = ["name", "logic"];

	// Parameters for saving
	this.save = ["ai_status", "name", "definition", "logic", "props"];

	// Save parameters in data
	this.save_data = ["bm_cell", "bm_type", "bm_s", "bm_aiolh", "bm_aiolv"];
	
	// Parameters that are displayed for saving
	this.save_display = ["bm_cell", "name", "bm_type", "bm_s", "logic", "bm_aiolh", "logic", "bm_aiolv"];

	// Mandatory parameters for retrieving
	this.retrieve_m = ["ai_status", "name", "definition"];
	
	// All parameters for retrieving
	this.retrieve = ["ai_id", "ai_status", "name", "definition"];

	// Update parameters
	this.update = ["aid_id", "prop_type_name", "value"];

	// Update device
	this.update_device = ["aid_id", "name", "logic"];

	// Approve parameters
	this.approve = ["aid_id", "prop_types"];
	
	this.all = ["id", "ai_id", "prop_statuses", "ai_status", "name", "props", "definition", "logic", "bm_cell", "bm_type", "bm_s", "bm_aiolh", "bm_aiolv"];

	this.id = "";
	this.ai_id = "";
	this.aid_id = "";
	this.ai_status = "";
	this.name = "";
	this.definition = "";
	this.logic = "";
	this.bm_cell = "";
	this.bm_type = "";
	this.bm_s = "";
	this.bm_aiolh = "";
	this.bm_aiolv = "";
	this.prop_statuses = "";

	this.props_raw = {};
	this.props = {};

	this.updateProps = function() {
		for(i=0; i<this.save_data.length; i++) {
 			this.props_raw[this.save_data[i]] = this[this.save_data[i]];
 		}

 		this.props = JSON.stringify(this.props_raw);
	}

	this.set = function(obj) {

		if(obj === undefined) {
 			return undefined;
 		}

 		for(i=0; i<this.all.length; i++) {
 			this[this.all[i]] = obj[this.all[i]];
 		}
	}

	if(obj !== undefined) {
 		this.set(obj);
 	}
});