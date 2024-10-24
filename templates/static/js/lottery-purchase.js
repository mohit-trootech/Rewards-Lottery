/**Lottery Purchase Page */
const slug = getLocationValidPath();
$(document).ready(() => {
  /**Trigger Function when Page Loaded */
  getLotteryDetail(slug, handlePurchase);
  getLoggedInUser();
});

function handlePurchase(lottery) {
  /**Handle Lottery Purchase */
  homeContent.innerHTML = `<div class="container mt-3">
  <div class="d-flex justify-content-start mb-3">
  <a class="btn btn-outline-primary shadow" href="/demo/" role="button">
  <i class="fa fa-arrow-left me-2"></i>
  Back to Lotteries
  </a></div
    <div class="d-flex flex-column justify-content-center align-items-center">
        <div class="col-md-4 mb-4 w-100">
            <h4 class="align-items-center mb-3">
                <span class="text-muted">Your cart</span>
                <span class="badge badge-secondary badge-pill">3</span>
            </h4>
            <ul class="list-group mb-3">
                <li class="list-group-item d-flex justify-content-between lh-condensed">
                    <div>
                        <h6 class="my-0">${lottery.title}</h6>
                         <small class="text-muted text-truncate mb-3">
                               ${lottery.description}
                            </small>
                    </div>
                    <span class="text-muted">$<strong  id="lotteryPrice">${lottery.price}</strong></span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center lh-condensed">
                    <div>
                        <h6 class="my-0">Quantity</h6>
                    </div>
                    <div class="">
                        <div class="input-group" style="width: 170px;">
                            <button class="btn btn-white border border-secondary px-3" type="button"
                                onclick="quantitySubtract()">
                                <i class="fas fa-minus"></i>
                            </button>
                            <input type="text" min="1" onchange="quantityChange(this)" readonly class="form-control text-center border border-secondary"
                                name="quantity" value="1" />
                            <button class="btn btn-white border border-secondary px-3" type="button" id="button-addon2"
                                onclick="quantityAdd()">
                                <i class="fas fa-plus"></i>
                            </button>
                        </div>
                    </div>
                </li>
                <li class="list-group-item d-flex justify-content-between">
                    <span>Total (USD)</span>
                    <span>$<strong id="lotteryTotal">${lottery.price}</strong></span>
                </li>
            </ul>
        </div>
    </div>
</div>
<button class="btn btn-outline-primary col-12 d-block" onclick="purchaseLottery('${lottery.slug}')">Purchase Lottery</button>
`;
  // paymentBtnRender();
}

function quantityAdd() {
  /**Add Lottery Quantity */
  const lotteryQuantity = document.querySelector("input[name=quantity]");
  lotteryQuantity.value = parseInt(lotteryQuantity.value) + 1;
  getLotteryCheckoutAmount(lotteryQuantity.value);
}
function quantitySubtract() {
  /**Subtract Lottery Quantity */
  const lotteryQuantity = document.querySelector("input[name=quantity]");
  if (lotteryQuantity.value <= 1) {
    lotteryQuantity.value = 1;
  } else {
    lotteryQuantity.value = parseInt(lotteryQuantity.value) - 1;
  }
  getLotteryCheckoutAmount(lotteryQuantity.value);
}
function quantityChange(elem) {
  /**Quantity on change */ lotteryTotal;
  if (elem.value < 1) {
    elem.value = 1;
  }
  elem.value < 1 ? (elem.value = 1) : elem.value;
  getLotteryCheckoutAmount(elem.value);
}
function getLotteryCheckoutAmount(quantity) {
  /**Get Lottery Checkout Amount */
  let lotteryTotal = document.getElementById("lotteryTotal");
  let lotteryPrice = document.getElementById("lotteryPrice");
  lotteryTotal.innerText = parseFloat(lotteryPrice.innerText) * quantity;
}

function purchaseLottery(slug) {
  /**Purchase Lottery */
  let user = window.localStorage.getItem("user") || getLoggedInUser();
  let quantity = parseInt(document.querySelector("[name=quantity]").value) || 1;

  patchRequest(
    `/api/lotteries/${slug}/?buyer=${user}&quantity=${quantity}`,
    null,
    purchaseLotteryHandle
  );
}

function purchaseLotteryHandle(response) {
  /**Handle Purchased Lottery */
  triggerToast("Succesfully Brought the Lottery");
}
