tree_names = [];
$("#sel option").each(function(idx){
    if (idx != 0) {
        tree_names.push($(this).attr("label"));
    };
});
console.log(JSON.stringify(tree_names));
