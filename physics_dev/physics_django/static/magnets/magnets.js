function ajgetcidesc(e) {
    var targ;
    if (!e)
        var e = window.event;
    if (e.target)
        targ = e.target;
    else if (e.srcElement)
        targ = e.srcElement;
    if (targ.nodeType == 3)// defeat Safari bug
        targ = targ.parentNode;
    var inventory_id = targ.id;
    gblinventoryid = inventory_id;
    // this hack: don't know how to pass the pv_id to the ajdisplaypvdesc callback
    var data = {
        'inventory_id' : inventory_id
    };
    //var url = "/magnets/web/inventoryprops/" + inventory_id + "/";
    var url = "/magnets/web/inventoryprops/";
    var args = {
        type : "GET",
        url : url,
        data : data,
        complete : ajdisplayinventoryprops
    };
    $.ajax(args);
    return false;
}

//javascript callback from ajupdatepvdesc
var ajdisplayinventoryprops = function(res, status) {// is status passed as a matter of course for all callbacks?
    if (status == "success") {
        var data = eval('(' + res.responseText + ')');
        // see the definitions of the args of the calling javascript 'ajupdatepvdesc'
        // it appears that res.responseText is the 'data' dictionary passed to the ajdisplaypvdesc callback

        // shouldn't this be data.inventory_idvar inventory_id = inventory_id;
        var serial_no = data.serial_no;
        var commonProps = data.commonProps;
        var current_1 = data.current_1;
        var up_dn = data.up_dn;
        var integral_xfer_func = data.integral_xfer_func;
        var B_ref_int = data.B_ref_int;
        var Roll_angle = data.Roll_angle;
        var meas_notes = data.meas_notes;
        var a1 = data.a1;
        var a2 = data.a2;
        var a3 = data.a3;
        var b1 = data.b1;
        var b2 = data.b2;
        var b3 = data.b3;
        var data_issues = data.data_issues;

        var alltext = '<div><table width="400" cellpadding="1">';
        alltext += '<tr><td>Serial Number</td><td>' + serial_no + '</td></tr>'
        alltext += '<tr><td>meas_coil_id</td><td>' + commonProps['meas_coil_id'] + '</td></tr>'
        alltext += '<tr><td>ref_radius</td><td>' + commonProps['ref_radius'] + '</td></tr>'
        alltext += '<tr><td>magnet_notes</td><td>' + commonProps['magnet_notes'] + '</td></tr>'
        alltext += '<tr><td>cond_curr</td><td>' + commonProps['cond_curr'] + '</td></tr>'
        alltext += '<tr><td>meas_loc</td><td>' + commonProps['meas_loc'] + '</td></tr>'
        alltext += '<tr><td>run_number</td><td>' + commonProps['run_number'] + '</td></tr>'
        alltext += '<tr><td>sub_device</td><td>' + commonProps['sub_device'] + '</td></tr>'
        alltext += '<tr><td>analysis_number</td><td>' + commonProps['analysis_number'] + '</td></tr>'
        alltext += '</table>'

        alltext += '<div class="xfer"><table class="xfer_table" border="1" cellpadding="1">';
        alltext += '<TH>current</TH><TH>up_dn</TH><TH>xfer_func</TH><TH>b_ref_int</TH><TH>roll</TH><TH>a1</TH><TH>a2</TH><TH>a3</TH><TH>b1</TH><TH>b2</TH><TH>b3</TH><TH>data issues</TH>'
        var len = current_1.length;
        for (var i = 0; i < len; i++) {
            alltext += '<tr>'
            alltext += '<td>' + current_1[i].toFixed(5) + '</td>'
            alltext += '<td>' + up_dn[i] + '</td>'
            alltext += '<td>' + integral_xfer_func[i].toFixed(5) + '</td>'
            alltext += '<td>' + B_ref_int[i].toFixed(7) + '</td>'
            alltext += '<td>' + Roll_angle[i].toFixed(5) + '</td>'
            //alltext += '<td>' + meas_notes[i] + '</td>'
            alltext += '<td>' + a1[i].toFixed(5) + '</td>'
            alltext += '<td>' + a2[i].toFixed(5) + '</td>'
            alltext += '<td>' + a3[i].toFixed(5) + '</td>'
            alltext += '<td>' + b1[i].toFixed(5) + '</td>'
            alltext += '<td>' + b2[i].toFixed(5) + '</td>'
            alltext += '<td>' + b3[i].toFixed(5) + '</td>'
            alltext += '<td>' + parseInt(data_issues[i]) + '</td>'
            alltext += '</>'
        }
        alltext += '</table></div>'

        //alert(alltext)
        $("#content1").html(alltext);
    } else
        alert("function failed.");
    //#?# needs to be fixed
}
// var ajupdatepvdesc = function() {
// var txt = $("#pvdesc_txt").val();
// var url = "/update_pvdesc/" + gblpvid + "/";
// var data = {pv_id:gblpvid, desc:txt};
// var args = { type:"POST", url:url, data:data, complete:ajdisplaypvdesc };
// $.ajax(args);
// return false;
// }
