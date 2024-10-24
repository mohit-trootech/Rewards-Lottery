/**Lotteries home js configuration */
$(document).ready(() => {
  /**When Lotteries Home Page Document Loaded */
  getRequest(lotteriesListUrl, handleLotteries);
});

function handleLotteries(content) {
  /**Handle Lotteries Content on Successfully Loading */

  if (content.results.length <= 0) {
    notAvailable("No Lotteries Available");
  } else {
    pagination(content.previous, content.next);
    loadLotteries(content.results);
  }
}

function loadLotteries(content) {
  /**Load Lotteries */
  const lotteries = document.getElementById("lotteries");
  lotteries.innerText = "";
  content.forEach((lottery) => {
    lotteries.innerHTML += `   <div class="row justify-content-center align-items-center mb-3">
        <div class="col-md-12">
            <div class="card shadow-0 border rounded-3" id="${lottery.slug}">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-12 col-lg-3 col-xl-3 mb-4 mb-lg-0">

                                <img src="${
                                  lottery.image
                                    ? lottery.image
                                    : "/static/img/empty.png"
                                }"
                                    class="card-img img-fluid h-100 object-fit-cover">
                        </div>
                        <div class="col-md-6 col-lg-6 col-xl-6" class="text-capitalize">
                            <h5>${lottery.title}</h5>
                            <div class="d-flex flex-row">
                                <div class="text-danger mb-1 me-2">
                                   <i class="fa fa-users-viewfinder me-1"></i>
                                   ${
                                     lottery.buyer_count < 5
                                       ? "New Purchase Now!"
                                       : `<span class="text-dark">
                                         ${lottery.buyer_count}
                                       </span> Already Purchased`
                                   }
                                </div>
                            </div>
                            <div class="mt-1 mb-0 text-muted small">
                                <span>${lottery.winning}$ Winning</span>
                                <span class="text-primary"> • </span>
                                <span>${lottery.total_draw} Draw</span>
                                <span class="text-primary"> • </span>
                                <span>${getFormattedDate(
                                  lottery.expiry_date
                                )} Draw Date</span>
                            </div>
                            <p class="text-truncate mb-3">
                               ${lottery.description}
                            </p>
                            <div>
                            <a role="button" href="${`/demo/profile/${lottery.vendor.username}/`}" class="border text-decoration-none rounded p-2 toast-header">
                                <img src="${
                                  lottery.vendor.image
                                    ? lottery.vendor.image
                                    : "/static/img/profile.jpg"
                                }" class="rounded-circle object-fit-cover me-2" height="32" width="32">
                                <strong class="me-auto">${
                                  lottery.vendor.username
                                }</strong>
                                <small>11 mins ago</small>
                            </a>
                        </div>
                        </div>
                        <div class="col-md-6 col-lg-3 col-xl-3 border-sm-start-none border-start">
                            <div class="d-flex flex-row align-items-center mb-1">
                                <h4 class="mb-1 overflow-hidden me-1">$${
                                  lottery.price
                                }</h4>
                            </div>
                            <marquee class="text-primary" direction="right">${"Lottery ".repeat(
                              10
                            )}</marquee>
                            <marquee class="text-danger" direction="left">${"Lottery ".repeat(
                              10
                            )}</marquee>
                            <marquee class="text-success" direction="right">${"Lottery ".repeat(
                              10
                            )}</marquee>
                            <div class="d-flex flex-column mt-4">
                                <a class="btn btn-primary lottery-detail btn-sm mb-3"
                                    type="button" href="/demo/lottery/${
                                      lottery.slug
                                    }">Details</a>
                                <a class="btn btn-outline-primary lottery-purchase btn-sm" href="/demo/purchase/${
                                  lottery.slug
                                }" type="button" href="/demo/purchase/${
      lottery.slug
    }">
                                    Purchase
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>`;
  });
}
