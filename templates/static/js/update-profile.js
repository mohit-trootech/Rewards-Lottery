/**Update Profile HTML */
const profileCard = document.getElementById("profile-card");
const profileDetails = document.getElementById("profile-details");
const updateModalDiv = document.getElementById("update-modal-div");
const addMoneyModalDiv = document.getElementById("add-money-modal-div");

function updateProfileCard(user) {
  /**Update Profile Card */
  profileCard.innerHTML = `
<div class="card mb-4">
    <div class="card-body text-center">
        <img src="${
          user.image || "/static/img/profile.jpg"
        }" alt="avatar" class="rounded-circle img-fluid px-3">
        <h5 class="my-3">${user.first_name || user.username}</h5>
        <p class="badge text-bg-primary text-light mb-1">${user.option}</p>
        <p class="text-muted mb-4">${
          user.address ||
          "<span class='text-muted'>Address Not Available</span>"
        }</p>
        ${
          user.username == window.localStorage.getItem("username")
            ? `
<div class="d-flex justify-content-center mb-2">
    <button type="button" class="btn btn-outline-primary ms-1" data-bs-toggle="modal" data-bs-target="#updateProfile">
        Update
    </button>
    <button type="button" class="btn btn-primary ms-1" data-bs-toggle="modal" data-bs-target="#addMoneyWallet">
        Add Money
    </button>
</div>`
            : ""
        }
    </div>
</div>`;
}

function updateProfileDetails(user) {
  /**Update Profile Details */
  profileDetails.innerHTML = `
<div class="card-body">
    <div class="row">
        <div class="col-sm-3">
            <p class="mb-0">Full Name</p>
        </div>
        <div class="col-sm-9">
            <p class="text-muted mb-0">${user.first_name || user.username}</p>
        </div>
    </div>
    <hr>
    <div class="row">
        <div class="col-sm-3">
            <p class="mb-0">Email</p>
        </div>
        <div class="col-sm-9">
            <p class="text-muted mb-0">${
              user.email || "Email Not Available"
            }</p>
        </div>
    </div>
    <hr>
    <div class="row">
        <div class="col-sm-3">
            <p class="mb-0">Phone</p>
        </div>
        <div class="col-sm-9">
            <p class="text-muted mb-0">
                ${user.phone || "Phone Not Available"}
            </p>
        </div>
    </div>
    <hr>
    <div class="row">
        <div class="col-sm-3">
            <p class="mb-0">Gender</p>
        </div>
        <div class="col-sm-9">
            <p class="text-muted mb-0">
                ${user.gender || "Gender Not Available"}
            </p>
        </div>
    </div>
    <hr>
    <div class="row">
        <div class="col-sm-3">
            <p class="mb-0">Address</p>
        </div>
        <div class="col-sm-9">
            <p class="text-muted mb-0">
                ${user.address || "Address Not Available"}
            </p>
        </div>
    </div>
    <hr>
    <div class="row">
        <div class="col-sm-3">
            <p class="mb-0">Balance</p>
        </div>
        <div class="col-sm-9">
            <p class="text-muted mb-0">
                ${user.wallet.balance || "Balance Not Available"}$
            </p>
        </div>
    </div>
</div>`;
}

function updateProfileModal(user) {
  /**Update Profile Modal */
  updateModalDiv.innerHTML = `
 <div class="modal fade" id="updateProfile" tabindex="-1" aria-labelledby="updateProfileLabel" aria-hidden="true">
        <form class="modal-dialog" onsubmit="updateProfile(event)">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="updateProfileLabel">Update Profile</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                        <div class="mb-3">
                            <label for="full_name" class="form-label">First Name</label>
                            <input type="text" class="form-control" name="first_name" value="${
                              user.first_name || ""
                            }" id="full_name"
                                aria-describedby="emailHelp">
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" name="email" value="${
                              user.email || ""
                            }" id="email">
                        </div>
                        <div class="mb-3">
                            <label for="phone" class="form-label">Phone Number</label>
                            <input type="tel" pattern="^[0-9]{10}$" value="${
                              user.phone || ""
                            }" class="form-control"
                                name="phone" id="phone">
                        </div>
                        <div class="mb-3">
                            <label for="address" class="form-label">Address</label>
                            <input type="text" class="form-control" name="address" value="${
                              user.address || ""
                            }" id="address">
                        </div>
                    </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-primary">Save changes</button>
                </div>
            </div>
        </form>
    </div>
`;
}

function addMoneyModal(user) {
  /**Add Money Modal */
  addMoneyModalDiv.innerHTML = `
<div class="modal fade" id="addMoneyWallet" tabindex="-1" aria-labelledby="addMoneyWalletLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="addMoneyWalletLabel">Modal title</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
            <label for="wallet" class="form-label">Current Wallet Balance: ${user.wallet.balance}$</label>
                <div class="input-group mb-3">
                    <input type="number" step="0.01" class="form-control" id="wallet" name="balance"
                        placeholder="Enter Amount to Add in Wallet">
                    <button class="btn btn-outline-primary" onclick="paymentBtnRender()" type="button">Confirm</button>
                </div>
                <div id="paypal-button-container"></div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            </div>
        </div>
    </div>
</div>
      `;
}

function paymentBtnRender() {
  /**Render Payment Button */
  const amount = document.getElementById("wallet").value;
  if (amount) {
    /**Open Paypal Dialog When Adding MOney */
    paypal
      .Buttons({
        createOrder: function (data, actions) {
          return actions.order.create({
            purchase_units: [
              {
                amount: {
                  value: amount,
                },
              },
            ],
          });
        },
        onApprove: function (data, actions) {
          return actions.order.capture().then(function (order) {
            paymentComplete(order);
          });
        },
      })
      .render("#paypal-button-container");
  } else {
    triggerToast("Enter a Valid Amount");
  }
}
function paymentComplete(order) {
  /**Complete Completed */
  let serialized_order = paymentResponseSerialize(order);
  postRequest("/api/orders/", paymentResponseSerialize(order), capturePayment);
}

function capturePayment(response) {
  /**Capture Payment Response */
  console.log(response);
  window.localStorage.setItem(
    "toastMessage",
    "Payment Successfull..., Amount Added in Wallet"
  );
  window.location.reload();
}
