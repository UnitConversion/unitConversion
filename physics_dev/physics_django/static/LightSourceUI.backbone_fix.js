
//Builds on the global LightSourceUI object
LightSourceUI.backbone = {};

//Define Backbone event handlers based on http://backbonejs.org/docs/backbone.html#section-173
LightSourceUI.backbone.ajaxHandlers = {
    error   : function (originalModel, resp, options) {
        LightSourceUI.showError('There was an error contacting the server'); 
    },
    //success only means the server responded, not that there is not an error_msg in the response
    success : function (model, resp) {
       if(resp.error_msg) {
            LightSourceUI.showError('There was an error: ' + resp.error_msg);  
       }
    }
};

//A Backbone utility model to track state using the hash and also generate a url
LightSourceUI.backbone.State_fix = Backbone.Model.extend({
        defaults : {},
        getQueryString : function (addParams) {
            var hashables = [];
            var dict = this.toJSON();
            
            // include added parameters at start so that they are included in defaults removal
            if (addParams) {
                for (key in addParams) {
                    dict[key] = addParams[key];
                }
            }
            
            for (key in dict) {
            	// indexOf returns -1 when element not present
                if((_.indexOf(_.keys(this.defaults), key) == -1 || (this.defaults[key] != dict[key])) && dict[key] != undefined ) {
                     hashables.push(key + '=' + escape(dict[key]));
                }
            }
            return '?' + hashables.join('&');
        },
        //A hash to use in the url to create a bookmark or link
        //Makes somehting like prop1:value1|prop2:value2
        //Pass additional parameters to be added to addParams
        getHash : function (addParams) {
            return this.getQueryString(addParams).substring(1).replace(/&/g, '|').replace(/=/g, ':');
        },
        //Take a hash from the url and set the model attributes
        //Parses from the formate of prop1:value1|prop2:value2
        setFromHash : function (hash) {
            var hashables = hash.split('|');
            // do not set defaults here to not override already set data
            var dict  = {};
            _.each(hashables, function (hashable) {
                var parts = hashable.split(':');
                var prop = parts[0];
                var value = parts[1]; 
                dict[prop] = value;
            });
           
            this.set(dict);
        }
    });