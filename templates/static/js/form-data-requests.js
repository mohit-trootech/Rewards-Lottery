/**Ajax Requests */

function formDataPostRequest(url, data, callback) {
  FormDataAjaxCall("POST", url, data, callback);
}

function formDataPatchRequest(url, data, callback) {
  FormDataAjaxCall("PATCH", url, data, callback);
}

function FormDataAjaxCall(type, url, data, callback) {
  $.ajax({
    url: url,
    type: type,
    data: data,
    headers: getHeaders(),
    processData: false,
    contentType: false,
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
