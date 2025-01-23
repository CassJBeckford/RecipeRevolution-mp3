document.addEventListener('DOMContentLoaded', function() {
    // Materialize sidenav initialisation (https://materializecss.com/navbar.html)
    let navbar = document.querySelectorAll('.sidenav');
    M.Sidenav.init(navbar);
});

document.addEventListener('DOMContentLoaded', function() {
    let category_collapse = document.querySelectorAll('.collapsible');
    M.Collapsible.init(category_collapse);
  });