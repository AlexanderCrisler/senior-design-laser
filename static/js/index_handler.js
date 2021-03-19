var current_item;
var itemname, input, filter, listbox, txtValue;

// Handles searching through listbox by matching substrings
function searchItem() {
   input = document.getElementById("searchbar");
   filter = input.value.toUpperCase();
   listbox = document.getElementById("items");
   
   for (i = 0; i < listbox.length; i++) {
      txtValue = listbox[i].textContent || listbox[i].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
         listbox[i].style.display = "";
      } else {
         listbox[i].style.display= "none";
      }
    }
};

// Calls selected_index function to move laser to item location
function highlight() {
   //window.alert("t")
   itemname = document.getElementById("items");
   var sent_info = { name: itemname[itemname.selectedIndex].innerHTML };
   fetch(`${window.origin}/selected_index`, {
		method:  "POST",
		credentials: "include",
		body: JSON.stringify(sent_info),
		cache: "no-cache",
		headers: new Headers({ "content-type": "application/json" })
   })
   .then(function (response) {
      response.json().then(function (data) {
      })
   })
};