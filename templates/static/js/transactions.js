/**Handle all Transactions Page Scripts */
const transactions_url = "/api/transaction/";

$(document).ready(() => {
  /**Trigger Function when Page Loaded */
  getRequest(transactions_url, handleTransactions);
});

function handleTransactions(response) {
  /**Handle User Tranasctions */
  var data = [];
  response.forEach((elem) => {
    /**Add Elements in Table */
    data.push([
      elem.id,
      `<img class="rounded-circle object-fit-cover me-2" height="32" width="32" src="${
        elem.user.image || "/static/img/profile.jpg"
      }" />`,
      elem.user.get_full_name || elem.user.username,
      `<span class="badge text-bg-primary">${elem.option}</span>`,
      elem.amount,
      elem.description,
      getFormattedDate(elem.created),
    ]);
  });

  let table = new DataTable("#myTable", {
    responsive: true,
    data: data,
  });
}
