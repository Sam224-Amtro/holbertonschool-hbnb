/* ==========================================================
   CONFIG API
   ========================================================== */
const API_URL = "http://localhost:5000/api/v1/";

/* ==========================================================
   AFFICHAGE UTILISATEUR SI CONNECTÉ
   ========================================================== */
function updateUserUI() {
    const token = localStorage.getItem("token");
    const userName = localStorage.getItem("user_name");

    const loginLink = document.querySelector(".nav-links a[href='login.html']");
    const userProfile = document.querySelector(".user-profile");
    const userNameSpan = document.querySelector(".user-name");

    if (token && userName) {
        if (loginLink) loginLink.style.display = "none";
        if (userProfile) userProfile.style.display = "flex";
        if (userNameSpan) userNameSpan.textContent = userName;
    } else {
        if (loginLink) loginLink.style.display = "block";
        if (userProfile) userProfile.style.display = "none";
    }
}

/* ==========================================================
   LOGIN
   ========================================================== */
async function handleLogin(e) {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    try {
        const response = await fetch(API_URL + "auth/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            alert("Login failed");
            return;
        }

        const data = await response.json();

        // On stocke le token + user
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("user_name", data.user.first_name);

        window.location.href = "index.html";

    } catch (error) {
        console.error("Login error:", error);
    }
}

/* ==========================================================
   LOGOUT
   ========================================================== */
function setupLogout() {
    const logoutBtn = document.querySelector(".logout-icon");

    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            localStorage.removeItem("token");
            localStorage.removeItem("user_name");
            window.location.reload();
        });
    }
}

/* ==========================================================
   CHARGER TOUTES LES PLACES
   ========================================================== */
async function fetchPlaces() {
    try {
        const response = await fetch(API_URL + "places/", {
            method: "GET"
        });

        if (!response.ok) throw new Error("Failed to fetch places");

        const places = await response.json();

        const placesContainer = document.querySelector(".places-list");
        if (!placesContainer) return;

        placesContainer.innerHTML = "";

        places.forEach(place => {
            const card = document.createElement("div");
            card.classList.add("place-card");

            card.innerHTML = `
                <h3>${place.title}</h3>
                <p>Price: $${place.price}</p>
                <a href="place.html?id=${place.id}" class="details-btn">View Details</a>
            `;

            placesContainer.appendChild(card);
        });

    } catch (error) {
        console.error("Error loading places:", error);
        alert("Error loading places: Failed to fetch places");
    }
}

/* ==========================================================
   CHARGER DETAILS D’UNE PLACE
   ========================================================== */
async function fetchPlaceDetails() {
    const params = new URLSearchParams(window.location.search);
    const placeId = params.get("id");

    if (!placeId) return;

    try {
        const response = await fetch(API_URL + `places/${placeId}`, {
            method: "GET",
        });

        if (!response.ok) throw new Error("Failed to fetch place");

        const place = await response.json();

        const container = document.querySelector(".place-details");
        if (!container) return;

        container.innerHTML = `
            <h1>${place.title}</h1>
            <p>${place.description || "No description available."}</p>
            <p><strong>Price:</strong> $${place.price}</p>
        `;

    } catch (error) {
        console.error("Error loading place details:", error);
    }
}

/* ==========================================================
   CHARGER LES REVIEWS
   ========================================================== */
async function fetchReviews() {
    const params = new URLSearchParams(window.location.search);
    const placeId = params.get("id");
    if (!placeId) return;

    try {
        const response = await fetch(API_URL + `places/${placeId}/reviews`, {
            method: "GET"
        });

        if (!response.ok) {
            console.warn("No reviews available");
            return;
        }

        const reviews = await response.json();
        const container = document.querySelector(".reviews-container");

        reviews.forEach(r => {
            const div = document.createElement("div");
            div.classList.add("review-item");

            div.innerHTML = `
                <strong>${r.user}</strong>
                <p>${r.text}</p>
                <span>Rating: ${r.rating}/5</span>
            `;

            container.appendChild(div);
        });

    } catch (error) {
        console.error("Error loading reviews:", error);
    }
}

/* ==========================================================
   INIT
   ========================================================== */
document.addEventListener("DOMContentLoaded", () => {
    updateUserUI();
    setupLogout();

    if (document.getElementById("loginForm")) {
        document.getElementById("loginForm").addEventListener("submit", handleLogin);
    }

    if (document.querySelector(".places-list")) {
        fetchPlaces();
    }

    if (document.querySelector(".place-details")) {
        fetchPlaceDetails();
        fetchReviews();
    }
});
