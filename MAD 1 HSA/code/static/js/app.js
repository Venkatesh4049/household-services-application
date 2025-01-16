document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("#loginForm");
    const registerForm = document.querySelector("#registerForm");
    const searchInput = document.querySelector("#searchServices");
    const acceptBtns = document.querySelectorAll(".accept-btn");
    // Form validation for login
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            const email = document.querySelector("#email").value;
            const password = document.querySelector("#password").value;
            if (!email || !password) {
                event.preventDefault();
                alert("Please enter both email and password.");
            }
        });
    }
    // Form validation for register
    if (registerForm) {
        registerForm.addEventListener("submit", function (event) {
            const username = document.querySelector("#username").value;
            const email = document.querySelector("#email").value;
            const password = document.querySelector("#password").value;
            const confirmPassword = document.querySelector("#confirm_password").value;
            if (!username || !email || !password || !confirmPassword) {
                event.preventDefault();
                alert("All fields are required.");
            } else if (password !== confirmPassword) {
                event.preventDefault();
                alert("Passwords do not match.");
            }
        });
    }
    // Service search functionality
    if (searchInput) {
        let debounceTimer;
        searchInput.addEventListener("input", function () {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(function () {
                const query = searchInput.value.toLowerCase();
                const serviceList = document.querySelectorAll(".service-item");
                let found = false;
                serviceList.forEach(function (item) {
                    const serviceName = item.querySelector(".service-name").textContent.toLowerCase();
                    if (serviceName.includes(query)) {
                        item.style.display = "block";
                        found = true;
                    } else {
                        item.style.display = "none";
                    }
                });
                const noResultsMessage = document.querySelector("#noResultsMessage");
                if (!found && noResultsMessage) {
                    noResultsMessage.style.display = "block";
                } else if (noResultsMessage) {
                    noResultsMessage.style.display = "none";
                }
            }, 300); 
        });
    }
    // Handling accept button click for service professionals
    acceptBtns.forEach(function (btn) {
        btn.addEventListener("click", function () {
            const serviceRequestId = btn.getAttribute("data-service-id");

            fetch(`/accept_service/${serviceRequestId}`, {
                method: "POST",
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        btn.classList.add("accepted");
                        alert("Service request accepted!");
                    } else {
                        alert("Failed to accept the service request.");
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                    alert("An error occurred. Please try again.");
                });
        });
    });
    // Login example
    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token() }}",
        },
        body: JSON.stringify({
            email: "example@example.com",
            password: "password",
        }),
    });
});
