// login.js

$(document).ready(function () {
    $('#login-form').on('submit', function (event) {
      event.preventDefault();
  
      $.ajax({
        type: 'POST',
        url: '/your-login-url/',
        data: $(this).serialize(),
        success: function (response) {
          if (response.success) {
            // Check if there's a redirect URL
            if (response.redirect_url) {
              // Redirect to the provided URL
              window.location.href = response.redirect_url;
            }
          } else {
            $('#error-message').html(response.message);
          }
        },
      });
    });
  });
  