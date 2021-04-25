
// Adds the item to the diciontary of all items once submitted.

// Window will listen for keyboard presses and call the laser moving function
// if the right key is pressed
function move_laser(key) {
   console.log(move_called)
   if (move_called == false) {
      move_called = true
      console.log("AA")
      fetch(`${window.origin}/add/key_press`, {
                  method:  "POST",
                  credentials: "include",
                  body: JSON.stringify(key),
                  cache: "no-cache",
                  headers: new Headers({ "content-type": "application/json" })
         })
         .then(function (response) {
            response.json().then(function (data) {
               setTimeout(move_called = false, 10000)
            })
        })
     }
}

var move_called = false
document.addEventListener('keydown', event => {
   console.log(move_called)
   if (move_called == false) {
      move_called = true
      console.log("AA")
      fetch(`${window.origin}/add/key_press`, {
                  method:  "POST",
                  credentials: "include",
                  body: JSON.stringify(event.keyCode),
                  cache: "no-cache",
                  headers: new Headers({ "content-type": "application/json" })
         })
         .then(function (response) {
            response.json().then(function (data) {
               setTimeout(move_called = false, 10000)
            })
         })
      }
   }
);