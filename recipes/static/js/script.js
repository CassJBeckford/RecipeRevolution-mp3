document.addEventListener('DOMContentLoaded', function() {
    // Materialize sidenav initialisation (https://materializecss.com/navbar.html)
    let navbar = document.querySelectorAll('.sidenav');
    M.Sidenav.init(navbar);


    let category_collapse = document.querySelectorAll('.collapsible');
    M.Collapsible.init(category_collapse);


    let delete_modal = document.querySelectorAll('.modal');
    M.Modal.init(delete_modal);


    let selects = document.querySelectorAll("select");
    M.FormSelect.init(selects);

});