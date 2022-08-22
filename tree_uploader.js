data_to_upload = []  // replace [] with your JSON tree data

options_data = {}
$("#sel option").each(function(idx){
    if (idx != 0) {
        options_data[$(this).attr("label")] = $(this).val();
    }
});

data_to_upload.forEach(function(tree, idx){
    console.log((idx+1) + ". tree: " + tree.name + " (" + tree.lat + ", " + tree.lon + ")");
    tree_id = options_data[tree.name];
    $("#pozicie").append('<input type="hidden" id="tree' + (idx+1) + '" name="tree[' + (idx+1) + ']" value="' + tree.lat + "," + tree.lon + "," + tree_id + '" />');
});

console.log("All trees have been entered even though you see no markers on the map. Press 'Save'/'Uložiť' to save all added trees.")
