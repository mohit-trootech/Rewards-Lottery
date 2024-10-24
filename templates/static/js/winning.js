/**Handle all Transactions Page Scripts */
const transactions_url = "/api/winners/";

$(document).ready(() => {
  /**Trigger Function when Page Loaded */
  getRequest(transactions_url, handleWinners);
});

function handleWinners(response) {
  /**Handle User Tranasctions */
  console.log(response);
  var data = [];
  response.forEach((elem) => {
    /**Add Elements in Table */
    data.push([
      elem.id,
      `<img class="rounded-circle object-fit-cover me-2" height="32" width="32" src="${
        elem.lottery.image || "/static/img/empty.png"
      }" />`,
      elem.lottery.title,
      elem.amount,
      getFormattedDate(elem.created),
    ]);
  });

  let table = new DataTable("#myTable", {
    responsive: true,
    data: data,
    // });
  });
}
