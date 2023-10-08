getCSRF = () => {
    fetch("/api/csrf/", {
      credentials: "same-origin",
    })
    .then((res) => {
      let csrfToken = res.headers.get("X-CSRFToken");
      console.log(csrfToken);
    })
    .catch((err) => {
      console.log(err);
    });
  }


getCSRF()
