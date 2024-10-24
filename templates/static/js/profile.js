/**Script for Profile */

const user = getLocationValidPath();

$(document).ready(() => {
  /**On Document Load Fetch User Details */
  getRequest(`/api/users/${user}/`, handleProfile);
});

function handleProfile(response) {
  /**Handle Profile Response */
  updateProfileCard(response);
  updateProfileDetails(response);
  if (response.username == window.localStorage.getItem("username")) {
    updateProfileModal(response);
    addMoneyModal(response);
  }
}

function updateProfile(event) {
  /**Handle Update Profile Form Submit */
  event.preventDefault();
  const profileFormData = new FormData(event.target);
  for (let [key, value] of profileFormData.entries()) {
    console.log(`${key}: ${value}`);
  }
  formDataPatchRequest(
    `/api/users/${window.localStorage.getItem("username")}/`,
    profileFormData,
    handleProfileUpdate
  );
}
function handleProfileUpdate(response) {
  /**Handle Profile Update */
  window.location.reload();
}
