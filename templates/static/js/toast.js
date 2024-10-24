const myToastEl = document.getElementById("myToast");
const myToastBody = document.getElementById("myToastBody");
var myToast = new bootstrap.Toast(myToastEl, {
  animation: true,
  autohide: true,
  delay: 5000,
});
