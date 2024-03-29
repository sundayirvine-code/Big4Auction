 document.addEventListener('DOMContentLoaded', function() {
  var stripeElements = function(publicKey, setupIntent) {
    var stripe = Stripe(publicKey);
    var elements = stripe.elements();
  
    // Element styles
    var style = {
      base: {
        fontSize: "15px",
        color: "#32325d",
        fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
        fontSmoothing: "antialiased",
        ':-webkit-autofill': {
          color: '#fce883',
        },
        "::placeholder": {
          color: "rgba(0,0,0,0.4)"
        }
      }
    };
    var card = elements.create("card", { style: style});
    card.mount("#card-element");
  
    // Element focus ring
    card.on("focus", function() {
      var el = document.getElementById("card-element");
      el.classList.add("focused");
    });
  
    card.on("blur", function() {
      var el = document.getElementById("card-element");
      el.classList.remove("focused");
    });
  
    // Handle payment submission when user clicks the pay button.
    var button = document.getElementById("submit");
    button.addEventListener("click", function(event) {
      event.preventDefault();
      changeLoadingState(true);
  
      stripe.confirmCardSetup(setupIntent.client_secret, {
          payment_method: {
            card: card,
          }
        })
        .then(function(result) {
          if (result.error) {
            console.log('error occured', result.error.message)
            changeLoadingState(false);
            var displayError = document.getElementById("card-errors");
            displayError.textContent = result.error.message;
          } else {
            // The PaymentMethod was successfully set up
            console.log('The PaymentMethod was successfully set up')
            orderComplete(stripe, setupIntent.client_secret, setupIntent.customer);
          }
        });
    });
  };

  var getSetupIntent = function(publicKey) {
    return fetch("/create-setup-intent", {
      method: "post",
      headers: {
        "Content-Type": "application/json",
      }
    })
      .then(function(response) {
        console.log('get setup intent responded',response)
        return response.json();
      })
      .then(function(setupIntent) {
        console.log('the set up intent', setupIntent)
        customerID = setupIntent.customer
        stripeElements(publicKey, setupIntent);
      });
  };

  var getPublicKey = function() {
    return fetch("/public-key", {
      method: "get",
      headers: {
        "Content-Type": "application/json"
      }
    })
      .then(function(response) {
        console.log('public key', response)
        return response.json();
      })
      .then(function(response) {
        getSetupIntent(response.publicKey);
      });
  };
  
  // Show a spinner on payment submission
  var changeLoadingState = function(isLoading) {
    if (isLoading) {
      document.querySelector("button").disabled = true;
      document.querySelector("#spinner").classList.remove("hidden");
      document.querySelector("#button-text").classList.add("hidden");
    } else {
      document.querySelector("button").disabled = false;
      document.querySelector("#spinner").classList.add("hidden");
      document.querySelector("#button-text").classList.remove("hidden");
    }
  };
  
  /* Shows a success / error message when the payment is complete */
  var orderComplete = function(stripe, clientSecret, customerID) {
    stripe.retrieveSetupIntent(clientSecret).then(function(result) {
      var setupIntent = result.setupIntent;
      var setupIntentJson = JSON.stringify(setupIntent, null, 2);
  
      document.querySelector(".sr-payment-form").classList.add("hidden");
      document.querySelector(".sr-result").classList.remove("hidden");
      document.querySelector("pre").textContent = setupIntentJson;
      setTimeout(function() {
        document.querySelector(".sr-result").classList.add("expand");
      }, 200);

      console.log(customerID)
      // Redirect to the registration page with the customer ID
      window.location.href = '/registration/' + customerID;

      changeLoadingState(false);
    });
  };
  
  getPublicKey();
});