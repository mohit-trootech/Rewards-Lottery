/**Logout Handle */
$(document).ready(() => {
  $("#logoutBtn").click(() => {
    /**User Logout */
    window.localStorage.removeItem("refreshToken");
    window.localStorage.removeItem("accessToken");
    window.location.reload();
  });
});
