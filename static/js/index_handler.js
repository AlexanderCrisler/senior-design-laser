var current_item;
var itemname, input, filter, listbox, txtValue;

input = document.getElementById("searchbar");

input.addEventListener("keyup", function(event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        document.getElementById("searchbutton").click();
    }
});

// Handles searching through listbox by matching substrings
function searchItem() {
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

function load_items_to_list() {
   fetch(`${window.origin}/get_all_items`, {
		method:  "GET",
		credentials: "include",
		cache: "no-cache",
		headers: new Headers({ "content-type": "application/json" })
   })
   .then(function (response) {
      response.json().then(function (data) {
         //console.log(data)
         select_box = document.getElementById('items')
         select_box.innerHTML = ''
         for (var i = 0; i < data[0].length; i++) {
            var option = document.createElement("option")
            option.innerHTML = data[0][i]
            select_box.appendChild(option)
         }
      })
   })
}
function deleteIndex() {
   itemname = document.getElementById("items");
   var sent_info = {name: itemname[itemname.selectedIndex].innerHTML}
   fetch(`${window.origin}/delete`, {
		method:  "POST",
		credentials: "include",
		body: JSON.stringify(sent_info),
		cache: "no-cache",
		headers: new Headers({ "content-type": "application/json" })
   })
   .then(function(response) {
       response.json().then(function (){})
   })
   console.log("Calling")
   load_items_to_list()
}