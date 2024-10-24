/**Utility For Lottery Demo */
function notAvailable(message) {
  /**Common Message with parameter to display Not Found Content */
  homeContent.innerHTML = `<div class="p-5 mb-4 bg-body-tertiary rounded-3 h-100">
      <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">Not Found</h1>
        <p class="col-md-8 fs-4">${message}</p>
        <img src='/static/img/404.jpg' %}" height="250"/>
      </div>
    </div>`;
}

function pagination(previous, next) {
  /**Handle Pagniation */
  !previous
    ? $("#page-item-previous").addClass("disabled")
    : previousPageHref();
  !next ? $("#page-item-next").addClass("disabled") : nextPageHref();
}

function previousPageHref() {
  /**Update Previous Page href based on current page search */
  let urlParams = new URLSearchParams(window.location.search);
  const prevText = "Previous";

  if (urlParams.has("page")) {
    let page = parseInt(urlParams.get("page"), 10);

    if (page > 1) {
      // Construct the URL with preserved parameters
      let newUrl = updatePageInURL(page - 1);
      $("#page-item-previous").html(
        `<a class="page-link" href="${newUrl}">${prevText}</a>`
      );
    }
  }
}

function nextPageHref() {
  /**Update Next Page href based on current page search */
  let urlParams = new URLSearchParams(window.location.search);
  const nextText = "Next";
  if (urlParams.has("page")) {
    let page = parseInt(urlParams.get("page"), 10);

    // Construct the URL with preserved parameters
    let newUrl = updatePageInURL(page + 1);
    $("#page-item-next").html(
      `<a class="page-link active" href="${newUrl}">${nextText}</a>`
    );
  } else {
    let newUrl = updatePageInURL(2);
    $("#page-item-next").html(
      `<a class="page-link active" href="${newUrl}">${nextText}</a>`
    );
  }
}

function updatePageInURL(newPage) {
  /** Updates the 'page' parameter in the URL while preserving others. */
  let urlParams = new URLSearchParams(window.location.search);
  urlParams.set("page", newPage);
  return "?" + urlParams.toString();
}

function triggerToast(message) {
  /**Trigget Toast Message */
  myToastBody.innerText = message;
  myToast.show();
}

function getFormattedDate(date) {
  /**Returns Formatted Date */
  const dateObject = new Date(date);

  const year = dateObject.getFullYear();
  const month = dateObject.toLocaleString("default", { month: "long" });
  const day = dateObject.getDate();

  return `${month} ${day}, ${year}`;
}

function getLotteryDetail(slug, callback) {
  /**Get Lottery Detail */
  getRequest("/api/lotteries/" + slug, callback);
}

function getLocationValidPath() {
  /**Returns Location Valid Path */
  let path = window.location.pathname.split("/");
  if (path[path.length - 1]) {
    /**if not slash in last place */
    return path[path.length - 1];
  }
  /**if slash in last place */
  return path[path.length - 2];
}

function getLotteryTotal() {
  /**Return Lottery Total in Float Format */
  return parseFloat(document.getElementById("lotteryTotal").innerText);
}

function paymentResponseSerialize(order) {
  /**Seriliaze Payment Response in Required API Format */
  return {
    id: order.id,
    payer: `${order.payer.name.given_name} ${order.payer.name.surname}`,
    email: order.payer.email_address,
    created: order.create_time,
    modified: order.update_time,
    status: order.status,
    amount: order.purchase_units[0].amount.value,
  };
}

function getLoggedInUser() {
  /**Get Logged in User ID */
  return getRequest("/api/logged_in_user/", updateLocalStorageUserID);
}

function updateLocalStorageUserID(content) {
  /**Get User ID in response and Update Local Storage for Logged in User */
  window.localStorage.setItem("user", content.id);
  window.localStorage.setItem("username", content.username);
  $("#dropdown-profile-link")
    ? $("#dropdown-profile-link").attr(
        "href",
        `/demo/profile/${content.username}/`
      )
    : "";
  $("#dropdown-profile-link")
    ? $("#dropdown-profile-img").attr(
        "src",
        content.image || "/static/img/profile.jpg"
      )
    : "";
  $("#dropdown-profile-name").html(content.username);

  return content.id;
}

function getHeaders() {
  /**Get Ajax Call Headers */
  let headers = {
    "X-Requested-With": "XMLHttpRequest",
  };
  if (window.localStorage.getItem("accessToken")) {
    headers["Authorization"] = `Bearer ${window.localStorage.getItem(
      "accessToken"
    )}`;
  }
  return headers;
}

function updateAccessToken(accessToken) {
  /**Update accessToken */
  window.localStorage.setItem("accessToken", accessToken);
}

function updateRefreshToken(refreshToken) {
  /**Update refreshToken */
  window.localStorage.setItem("refreshToken", refreshToken);
}

function removeAccessToken() {
  /**remove accessToken */
  window.localStorage.removeItem("accessToken");
}

function removeRefreshToken() {
  /**remove refreshToken */
  window.localStorage.removeItem("refreshToken");
}
