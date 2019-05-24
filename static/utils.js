/**
* populates the group selection tickboxes and assigns an event listener
**/
function create_groups_tickboxes(groups){
    var container = $("#options #groups")
    container.append("groups: <br>")
    for (var i=0; i<groups.length; i++){
        var group_name = groups[i]
        container
            .append("<label>"+group_name+"</label>")
            .append("<input type='checkbox' checked id='"+group_name+"'>")
    }
    container.find("input[type=checkbox]").change(function(){
        update()
    });
}

/**
* returns a list of selected group ids
**/
function get_selected_groups(){
    selected = []
    $('#options #groups input[type=checkbox]:checked').each(function(){
        selected.push($(this).attr('id'))
    })
    return selected
}
