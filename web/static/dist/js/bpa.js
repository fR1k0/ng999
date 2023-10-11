// Start: app.html 
function searchItems() {
        
    var searchInput = document.getElementById("searchInput");
    var filter = searchInput.value.toLowerCase(); 
    var items = document.getElementsByClassName("card w-100");

    var ctgryItemCount = {};

    for (var i = 0; i < items.length; i++) {
      var itemElement = items[i].querySelector("#formName"); 
      
      var itemName = itemElement.getAttribute("data-name").toLowerCase();
      var category = itemElement.getAttribute("data-id");

      if (!ctgryItemCount[category]) {
        ctgryItemCount[category] = 0;
      }

      ctgryItemCount[category]++;
      
      var content = category + "-content";
      var tab = category + "-tab";
      
      var displayContent = document.getElementById(content);
      var displayTab = document.getElementById(tab);

      if ((itemName.includes(filter) || itemName.indexOf(filter) !== -1) && filter !== "") {
        
        displayContent.classList.add("show");
        displayTab.classList.remove("collapsed");
        displayTab.setAttribute("aria-expanded", "true");
        items[i].style.display = "block";
      
      } else {

        ctgryItemCount[category]--;

        if (displayTab.getAttribute("aria-expanded")) {

          // hide all not related tab-content
          if (filter != "") {
            items[i].style.display = "none";
          }
          
        }

        // close all the tab-content if search is blank
        if (filter == "") {
          displayContent.classList.remove("show");
          displayTab.classList.add("collapsed");
          displayTab.setAttribute("aria-expanded", "false");
          items[i].style.display = "block";
        }
      
      }
    }

    // use to close the tab-content with zero content
    for (var category in ctgryItemCount) {

      if (ctgryItemCount[category] == 0) {

        var content = category + "-content";
        var tab = category + "-tab";
        
        var displayContent = document.getElementById(content);
        var displayTab = document.getElementById(tab);

        displayContent.classList.remove("show");
        displayTab.classList.add("collapsed");
        displayTab.setAttribute("aria-expanded", "false");
      }

    }

}
// End: app.html 