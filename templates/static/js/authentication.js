document.addEventListener("DOMContentLoaded", () => {
  /**Check Authenticated */
  const toastMessage = localStorage.getItem("toastMessage");
  if (toastMessage) {
    triggerToast(toastMessage);
    localStorage.removeItem("toastMessage");
  }

  if (
    !["/demo/login", "/demo/login/", "/demo/signup", "/demo/signup/"].includes(
      window.location.pathname
    )
  ) {
    /**Check if Location in Login or Signup */
    if (
      window.localStorage.getItem("accessToken") &&
      window.localStorage.getItem("refreshToken")
    ) {
      getLoggedInUser();
    } else {
      localStorage.setItem("toastMessage", "Please Login to Continue..");
      window.location = "/demo/login";
    }
  }
});
