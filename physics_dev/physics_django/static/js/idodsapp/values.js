/*
 * Values for insertion device online data service module
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 * @created: Feb 28, 2014
 */

app.value('EntityError', function(key, value){
	this.errorDict = {};
	this.num = 0;

	this.add = function(key, value) {
		this.errorDict[key] = value;
		this.num ++;
	}

	this.reset = function() {
		this.errorDict = {};
		this.num = 0;
	}

	if (key !== undefined && value !== undefined) {
		this.add(key, value);
		this.num ++;
	}
});

 app.value('Vendor', function(obj){
 	this.m = ["name"];
 	this.retrieve = ["id", "name", "description"];
 	this.list = ["name", "description"];
 	this.save = ["name", "description"];
 	this.update = ["old_name", "name", "description"];
 	this.display = {"name": "Name", "description": "Description", "id": "Id"};
 	this.id = "";
 	this.old_name = "";
 	this.name = "";
 	this.description = "";

 	this.set = function(obj) {

 		if(obj === undefined) {
 			return undefined;
 		}
 		
 		if('id' in obj) {
 			this.id = obj.id;
 		}
 		this.name = obj.name;
 		this.old_name = obj.name;
 		this.description = obj.description;
 	}

 	if(obj !== undefined) {
 		this.set(obj);
 	}

 	this.check = function() {

 	}
 });