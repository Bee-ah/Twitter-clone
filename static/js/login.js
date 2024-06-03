document.addEventListener('htmx:afterOnLoad', function(event) {
    var response = event.detail.xhr.response;
    var data = JSON.parse(response);
    if (data.success) {
      document.getElementById('login-error').innerText = "";
      window.location.replace(data.redirect_url);
    }
    if (!data.success) {
        document.getElementById('login-error').innerText = data.error_message;
    }
});