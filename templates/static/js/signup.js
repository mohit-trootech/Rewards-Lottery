document.addEventListener("DOMContentLoaded", () => {
  /**After DOM Content Loaded Update Dropdown Menu Options */
  const dropdown = document.getElementById("sidebar-dropdown");
  dropdown.innerHTML = `
    <li>
        <a class="dropdown-item" href="/demo/login/">
            Login
        </a>
    </li>
    <li>
        <a class="dropdown-item" href="/demo/signup/">
            Signup
        </a>
    </li>`;
});

document.addEventListener("submit", (event) => {
  /**Form Submit Event Listener */
  event.preventDefault();
  username = event.target.username.value;
  password = event.target.password.value;
  age = event.target.age.value;
  email = event.target.email.value;
  confirm_password = event.target.confirm_password.value;
  if (username && password) {
    /**Continue Login */
    postRequest(
      "/accounts/signup/",
      {
        username: username,
        password: password,
        age: age,
        email: email,
        confirm_password: confirm_password,
      },
      signUpSuccess
    );
  } else {
    /**Username & Passwords are Required Fields */
    triggerToast("Username & Password are Required Fields");
  }
});

function signUpSuccess(response) {
  /**Handle Successfull login */
  console.log(response);
  window.localStorage.setItem("toastMessage", "Registered Successfull...");
  window.location = "/demo/login";
}
