/**Ajax Requests */

function getRequest(url, callback) {
  ajaxCall("GET", url, null, callback);
}

function postRequest(url, data, callback) {
  ajaxCall("POST", url, data, callback);
}

function patchRequest(url, data, callback) {
  ajaxCall("PATCH", url, data, callback);
}

function ajaxCall(type, url, data, callback) {
  $.ajax({
    url: url,
    type: type,
    data: data,
    headers: getHeaders(),
    success: function (response, status, xhr) {
      console.log(xhr);
      if (xhr.status != 204) {
        if (callback) {
          callback(response);
        }
      }
    },
    error: function (xhr, status, error) {
      console.error("Error occurred:", xhr.responseText, status, error);
      triggerToast(
        `${Object.values(xhr.responseJSON)[0]} ${xhr.statusText}, ${xhr.status}`
      );
      if (xhr.status == 404) {
        /**If Status 404 Not found then Update Home page HTML */
        notAvailable(
          `${Object.values(xhr.responseJSON)[0]} ${xhr.statusText}, ${
            xhr.status
          }`
        );
      }
      if (xhr.status == 401) {
        tokenValidity();
      }
    },
  });
}
