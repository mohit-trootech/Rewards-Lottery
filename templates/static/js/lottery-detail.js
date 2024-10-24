/**Handle all Lottery Details Page Scripts */
const slug = getLocationValidPath();

$(document).ready(() => {
  /**Trigger Function when Page Loaded */
  getLotteryDetail(slug, handleLotteryDetail);
});

function handleLotteryDetail(lottery) {
  /**Update Lottery Details Page */
  homeContent.innerHTML = `<section class="mt-3 mx-0 px-0">
    <div class="container">
        <div class="row">
            <aside class="col-lg-6">
                <div class="border rounded-4 mb-3 d-flex justify-content-center">
                    <img class="rounded-4 shadow w-100 mx-auto object-fit-cover img-thumbnail"
                        src="${
                          lottery.image
                            ? lottery.image
                            : "/static/img/empty.png"
                        }" />
                </div>
            </aside>
            <main class="col-lg-6">
                <div class="ps-lg-3">
                    <h4 class="title text-dark">
                        ${lottery.title}
                    </h4>
                    <div class="d-flex flex-row">
                        <div class="text-danger mb-1 me-2">
                            <i class="fa fa-users-viewfinder me-1"></i>
                            ${
                              lottery.buyers.length < 5
                                ? "New Purchase Now!"
                                : `<span class="text-dark">
                                ${lottery.buyers.length}
                                </span> Already Purchased`
                            }
                        </div>
                    </div>
                    <div class="mb-3">
                        <span class="h5">$${lottery.price}</span>
                        <span class="text-muted">/per piece</span>
                    </div>
                    <p>
                        ${lottery.description}
                    </p>
                    <div class="row">
                        <dt class="col-3">Winning:</dt>
                        <dd class="col-9">$${lottery.winning}</dd>
                        <dt class="col-3">Draw</dt>
                        <dd class="col-9">${lottery.total_draw}</dd>
                        <dt class="col-3">Draw Date</dt>
                        <dd class="col-9">${getFormattedDate(
                          lottery.expiry_date
                        )}</dd>
                    </div>

                    <hr />
                    <div role="button" href="${
                      lottery.vendor.url
                    }" class="border vendor-detail rounded p-2 mb-3 toast-header">
                        <img src="${
                          lottery.vendor.image
                            ? lottery.vendor.image
                            : " /static/img/profile.jpg"
                        }"
                            class="rounded-circle object-fit-cover me-2" height="32" width="32">
                        <strong class="me-auto">${
                          lottery.vendor.username
                        }</strong>
                        <small>11 mins ago</small>
                    </div>
                    <div class="d-flex flex-column align-items-start">
                        <div class="">
                            <a class="btn btn-warning shadow-0" href="/demo/purchase/${
                              lottery.slug
                            }">
                                Buy now </a>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
</section>`;
}
