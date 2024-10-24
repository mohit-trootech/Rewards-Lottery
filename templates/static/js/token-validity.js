/**Check Token Validity */

function tokenValidity() {
  /**If token already Available and still get Unauthorization Error*/
  if (window.localStorage.getItem("refreshToken")) {
    postRequest(
      "/accounts/token/refresh/",
      { refresh: window.localStorage.getItem("refreshToken") },
      tokenRefreshSuccess
    );
  } else {
    removeAccessToken();
    removeRefreshToken();
  }
}

function tokenRefreshSuccess(response) {
  /**On Successfull Token Refresh */
  updateAccessToken(response.access);
  updateRefreshToken(response.refresh);
  window.location.reload();
}
