
// Adds the item to the diciontary of all items once submitted.

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