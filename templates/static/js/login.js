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
  if (username && password) {
    /**Continue Login */
    postRequest(
      "/accounts/login/",
      { username: username, password: password },
      loginSuccess
    );
  } else {
    /**Username & Passwords are Required Fields */
    triggerToast("Username & Password are Required Fields");
  }
});

function loginSuccess(response) {
  /**Handle Successfull login */
  window.localStorage.setItem("toastMessage", "Login Successfull...");
  window.localStorage.setItem("refreshToken", response.refresh);
  window.localStorage.setItem("accessToken", response.access);
  window.location = "/demo";
}
