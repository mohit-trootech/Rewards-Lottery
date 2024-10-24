/**Create Lottery Instance */
document.addEventListener("submit", (event) => {
  event.preventDefault();
  let formData = new FormData(event.target);
  for (let [key, value] of formData.entries()) {
    console.log(`${key}: ${value}`);
  }
  formDataPostRequest(lotteriesListUrl, formData, lotteryCreated);
});

function lotteryCreated(content) {
  /**Lottery created successfully callback */
  console.log(content);
}
