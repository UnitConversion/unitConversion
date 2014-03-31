/*
 * Values for active interlock
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 * @created: Mar 7, 2014
 */

/*
 * History object
 */
app.value('History', function(obj) {
	
	this.retrieve_display = ["description", "created_by", "created_date", "modified_by", "modified_date"];

	// All possible parameters
	this.all = ["id", "description", "created_by", "created_date", "modified_by", "modified_date"];

	this.id = "";
	this.description = "";
	this.created_by = "";
	this.created_date = "";
	this.modified_by = "";
	this.modified_date = "";

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
 * Logic object
 */
app.value('Logic', function(obj) {
	// Mandatory parameters for saving
	this.save_m = ["name", "code"];

	// Parameters for saving
	this.save = ["name", "shape", "logic", "code"];
	
	// Mandatory parameters for retrieving
	this.retrieve_m = ["name"];

	// Parameters for updating
	this.update = ["id", "name", "shape", "logic", "code", "status"];
	
	// All parameters for retrieving
	this.retrieve = ["name", "shape", "logic", "code", "status"];
	
	this.all = ["id", "name", "shape", "logic", "code", "status", "num"];

	this.id = "";
	this.name = "";
	this.shape = "";
	this.logic = "";
	this.code = "";
	this.status = "";
	this.num = "";

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
	this.retrieve_m = ["name", "definition"];
	
	// All parameters for retrieving
	this.retrieve = ["ai_id", "ai_status", "name", "definition"];

	// Update parameters
	this.update = ["aid_id", "prop_type_name", "value"];

	// Update device
	this.update_device = ["aid_id", "name", "logic"];

	// Approve parameters
	this.approve = ["aid_id", "prop_types"];

	// Cells that need to be approved after saving
	this.approvable = {"bm_aiolh":true, "bm_aiolv":true};
	
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

/*
 * Insertion device object
 */
app.value('InsertionDevice', function(obj) {
	// Mandatory parameters for saving
	this.save_m = ["name", "logic"];

	// Parameters for saving
	this.save = ["ai_status", "name", "definition", "logic", "props"];

	// Save parameters in data
	this.save_data = ["cell", "type", "set", "str_sect", "defined_by", "pos", "pos_from_cent", "safe_current", "x_max_offset", "x_max_angle", "x_extra_offset", "x_lat_name_s1", "x_lat_pos_s1", "x_pos_from_cent_s1", "x_offset_s1", "x_logic_1", "x_lat_name_s2", "x_lat_pos_s2", "x_pos_from_cent_s2", "x_offset_s2", "x_lat_pos_s3", "x_pos_from_cent_s3", "x_offset_s3", "x_logic_2", "x_angle", "y_max_offset", "y_max_angle", "y_extra_offset", "y_lat_name_s1", "y_lat_pos_s1", "y_pos_from_cent_s1", "y_offset_s1", "y_logic_1", "y_lat_name_s2", "y_lat_pos_s2", "y_pos_from_cent_s2", "y_offset_s2", "y_lat_pos_s3", "y_pos_from_cent_s3", "y_offset_s3", "y_logic_2", "y_angle"];
	
	// Parameters that are displayed for saving
	this.save_display = ["cell", "type", "set", "str_sect", "logic", "shape", "defined_by", "name", "pos", "pos_from_cent", "safe_current", "x_max_offset", "x_max_angle", "x_extra_offset", "x_lat_name_s1", "x_lat_pos_s1", "x_pos_from_cent_s1", "x_offset_s1", "x_logic_1", "x_lat_name_s2", "x_lat_pos_s2", "x_pos_from_cent_s2", "x_offset_s2", "x_lat_pos_s3", "x_pos_from_cent_s3", "x_offset_s3", "x_logic_2", "x_angle", "y_max_offset", "y_max_angle", "y_extra_offset", "y_lat_name_s1", "y_lat_pos_s1", "y_pos_from_cent_s1", "y_offset_s1", "y_logic_1", "y_lat_name_s2", "y_lat_pos_s2", "y_pos_from_cent_s2", "y_offset_s2", "y_lat_pos_s3", "y_pos_from_cent_s3", "y_offset_s3", "y_logic_2", "y_angle"];

	// Mandatory parameters for retrieving
	this.retrieve_m = ["name", "definition"];
	
	// All parameters for retrieving
	this.retrieve = ["ai_id", "ai_status", "name", "definition"];

	// Update parameters
	this.update = ["aid_id", "prop_type_name", "value"];

	// Update device
	this.update_device = ["aid_id", "name", "logic"];

	// Approve parameters
	this.approve = ["aid_id", "prop_types"];

	// Cells that need to be approved after saving
	this.approvable = {"x_max_offset": true, "x_max_angle": true, "x_extra_offset": true, "x_lat_name_s1": true, "x_lat_pos_s1": true, "x_pos_from_cent_s1": true, "x_offset_s1": true, "x_logic_1": true, "x_lat_name_s2": true, "x_lat_pos_s2": true, "x_pos_from_cent_s2": true, "x_offset_s2": true, "x_lat_pos_s3": true, "x_pos_from_cent_s3": true, "x_offset_s3": true, "x_logic_2": true, "x_angle": true, "y_max_offset": true, "y_max_angle": true, "y_extra_offset": true, "y_lat_name_s1": true, "y_lat_pos_s1": true, "y_pos_from_cent_s1": true, "y_offset_s1": true, "y_logic_1": true, "y_lat_name_s2": true, "y_lat_pos_s2": true, "y_pos_from_cent_s2": true, "y_offset_s2": true, "y_lat_pos_s3": true, "y_pos_from_cent_s3": true, "y_offset_s3": true, "y_logic_2": true, "y_angle": true};

	this.all = ["id", "ai_id", "prop_statuses", "ai_status", "name", "props", "definition", "logic", "shape", "cell", "type", "set", "str_sect", "defined_by", "pos", "pos_from_cent", "safe_current", "x_max_offset", "x_max_angle", "x_extra_offset", "x_lat_name_s1", "x_lat_pos_s1", "x_pos_from_cent_s1", "x_offset_s1", "x_logic_1", "x_lat_name_s2", "x_lat_pos_s2", "x_pos_from_cent_s2", "x_offset_s2", "x_lat_pos_s3", "x_pos_from_cent_s3", "x_offset_s3", "x_logic_2", "x_angle", "y_max_offset", "y_max_angle", "y_extra_offset", "y_lat_name_s1", "y_lat_pos_s1", "y_pos_from_cent_s1", "y_offset_s1", "y_logic_1", "y_lat_name_s2", "y_lat_pos_s2", "y_pos_from_cent_s2", "y_offset_s2", "y_lat_pos_s3", "y_pos_from_cent_s3", "y_offset_s3", "y_logic_2", "y_angle"];

	this.cell = "";
	this.type = "";
	this.set = "";
	this.str_sect = "";
	this.defined_by = "";
	this.pos = "";
	this.pos_from_cent = "";
	this.x_max_offset = "";
	this.x_max_angle = "";
	this.x_extra_offset = "";
	this.x_lat_name_s1 = "";
	this.x_lat_pos_s1 = "";
	this.x_pos_from_cent_s1 = "";
	this.safe_current = "";
	this.x_offset_s1 = "";
	this.x_logic_1 = "";
	this.x_lat_name_s2 = "";
	this.x_lat_pos_s2 = "";
	this.x_pos_from_cent_s2 = "";
	this.x_offset_s2 = "";
	this.x_lat_pos_s3 = "";
	this.x_pos_from_cent_s3 = "";
	this.x_offset_s3 = "";
	this.x_logic_2 = "";
	this.x_angle = "";
	this.y_max_offset = "";
	this.y_max_angle = "";
	this.y_extra_offset = "";
	this.y_lat_name_s1 = "";
	this.y_lat_pos_s1 = "";
	this.y_pos_from_cent_s1 = "";
	this.y_offset_s1 = "";
	this.y_logic_1 = "";
	this.y_lat_name_s2 = "";
	this.y_lat_pos_s2 = "";
	this.y_pos_from_cent_s2 = "";
	this.y_offset_s2 = "";
	this.y_lat_pos_s3 = "";
	this.y_pos_from_cent_s3 = "";
	this.y_offset_s3 = "";
	this.y_logic_2 = "";
	this.y_angle = "";

	this.id = "";
	this.ai_id = "";
	this.aid_id = "";
	this.ai_status = "";
	this.name = "";
	this.definition = "";
	this.logic = "";
	this.prop_statuses = "";

	this.props_raw = {};
	this.props = {};

	this.updateProps = function() {
		for(i=0; i<this.save_data.length; i++) {
 			this.props_raw[this.save_data[i]] = this[this.save_data[i]];
 		}

 		this.props = JSON.stringify(this.props_raw);
	}

	this.setObj = function(obj) {

		if(obj === undefined || this.all === undefined) {
 			return undefined;
 		}

 		for(i=0; i<this.all.length; i++) {
 			this[this.all[i]] = obj[this.all[i]];
 		}
	}

	if(obj !== undefined) {
 		this.setObj(obj);
 	}
});