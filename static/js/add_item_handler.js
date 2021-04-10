
// Adds the item to the diciontary of all items once submitted
function add_item_click() {

    sent_info = {name: document.getElementById("itemName").value}
    fetch(`${window.origin}/add/submit`, {
		method:  "POST",
		credentials: "include",
		body: JSON.stringify(sent_info),
		cache: "no-cache",
		headers: new Headers({ "content-type": "application/json" })
   })
   window.location = window.origin
}

// Window will listen for keyboard presses and call the laser moving function
// if the right key is pressed
document.addEventListener('keydown', event => {
    fetch(`${window.origin}/add/key_press`, {
                method:  "POST",
                credentials: "include",
                body: JSON.stringify(event.keyCode),
                cache: "no-cache",
                headers: new Headers({ "content-type": "application/json" })
       })
       .then(function (response) {
          response.json().then(function (data) {
          })
       })
    }
);