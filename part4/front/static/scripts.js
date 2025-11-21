// ----------------------- INITIALIZATION -----------------------
document.addEventListener('DOMContentLoaded', () => {
    // Vérification de l'authentification
    checkAuthentication();

    // Configuration du bouton de déconnexion
    setupLogout();

    // Configuration du filtre de prix sur la page d'accueil
    setupPriceFilter();

    // Gestion du formulaire de connexion
    const loginForm = document.querySelector('.form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = loginForm.querySelector('input[type="email"]').value;
            const password = loginForm.querySelector('input[type="password"]').value;
            await loginUser(email, password);
        });
    }

    // Gestion des pages spécifiques
    const pathname = window.location.pathname;

    if (pathname.includes('place.html')) {
        // Page de détail d'un lieu
        const placeId = new URLSearchParams(window.location.search).get('id');
        if (placeId) {
            fetchPlaceDetails(placeId);
            fetchReviews(placeId);
        } else {
            showError('Place ID not found');
        }
    } else if (document.getElementById('places-list')) {
        // Page d'accueil, liste des lieux
        fetchPlaces();
    }

    // Gestion du formulaire d'ajout de review
    const reviewForm = document.getElementById('reviewForm');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            handleReviewFormSubmit();
        });
    }
});

// ----------------------- AUTHENTICATION -----------------------
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function checkAuthentication() {
    const token = getCookie('token');
    const navLinks = document.querySelector('.nav-links');
    const userProfile = document.querySelector('.user-profile');

    if (token) {
        fetchUserInfo(token);
        if (userProfile) userProfile.style.display = 'flex';
        if (navLinks) hideLoginLinks(navLinks);
    } else {
        if (userProfile) userProfile.style.display = 'none';
        if (navLinks) showLoginLinks(navLinks);

        if (window.location.pathname.includes('add_review.html')) {
            window.location.href = 'login.html';
        }
    }
}

function hideLoginLinks(navLinks) {
    navLinks.querySelectorAll('a[href="login.html"]').forEach(link => link.style.display = 'none');
}

function showLoginLinks(navLinks) {
    navLinks.querySelectorAll('a[href="login.html"]').forEach(link => link.style.display = 'block');
}

function setupLogout() {
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) logoutButton.addEventListener('click', logout);

    const logoutIcon = document.querySelector('.logout-icon');
    if (logoutIcon) logoutIcon.addEventListener('click', logout);
}

function logout() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = 'index.html';
}

async function loginUser(email, password) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            const errorData = await response.json();
            return showError(errorData.message || 'Login failed');
        }

        const data = await response.json();
        const date = new Date();
        date.setTime(date.getTime() + 24 * 60 * 60 * 1000); // 1 jour
        document.cookie = `token=${data.access_token}; expires=${date.toUTCString()}; path=/; Secure; SameSite=Lax`;
        window.location.href = '/index.html';
    } catch (error) {
        showError('Erreur de connexion au serveur');
    }
}

async function fetchUserInfo(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/users/me', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) return;
        const user = await response.json();
        displayUserProfile(user);
    } catch (error) {
        console.error('Error fetching user info:', error);
    }
}

function displayUserProfile(user) {
    const userProfile = document.querySelector('.user-profile');
    if (!userProfile) return;
    const name = userProfile.querySelector('.user-name');
    if (name) name.textContent = user.first_name;
    setupLogout();
}

// ----------------------- PRICE FILTER -----------------------
function setupPriceFilter() {
    const priceFilter = document.querySelector('.price-filter select');
    if (!priceFilter) return;
    priceFilter.addEventListener('change', (e) => filterPlacesByPrice(e.target.value));
}

function filterPlacesByPrice(price) {
    const places = document.querySelectorAll('.place-card');
    const priceFilter = document.querySelector('.price-filter');
    let hasVisiblePlaces = false;

    const oldMessage = priceFilter.querySelector('.no-results');
    if (oldMessage) oldMessage.remove();

    const noResults = document.createElement('div');
    noResults.className = 'no-results';
    noResults.textContent = 'No places found for this price range';
    noResults.style.display = 'none';
    priceFilter.appendChild(noResults);

    places.forEach(place => {
        const priceElement = place.querySelector('.price');
        if (!priceElement) return;

        const placePrice = parseInt(priceElement.textContent.replace(/[^0-9]/g, ''));
        const priceMatch = place.querySelector('.price-match');

        if (price === 'all' || placePrice <= parseInt(price)) {
            place.style.display = 'block';
            if (priceMatch) {
                priceMatch.textContent = placePrice === parseInt(price) ? '✓ Exact price match' : `$${placePrice} (under budget)`;
                priceMatch.style.color = placePrice === parseInt(price) ? 'var(--secondary-color)' : 'var(--accent-color)';
            }
            hasVisiblePlaces = true;
        } else {
            place.style.display = 'none';
            if (priceMatch) priceMatch.textContent = '';
        }
    });

    noResults.style.display = hasVisiblePlaces ? 'none' : 'block';
}

// ----------------------- PLACES -----------------------
const placeImages = [
    'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80',
    'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80',
    'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80',
    'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&auto=format&fit=crop&w=1473&q=80'
];

function getRandomPlaceImage() {
    return placeImages[Math.floor(Math.random() * placeImages.length)];
}

async function fetchPlaces(token = null) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '<div class="loading">Loading places...</div>';
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch('http://localhost:5000/api/v1/places', { headers });
        if (!response.ok) throw new Error('Failed to fetch places');

        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        placesList.innerHTML = `<div class="error-message">Error loading places: ${error.message}</div>`;
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';
    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        const price = parseInt(place.price);

        placeCard.innerHTML = `
            <img src="${getRandomPlaceImage()}" alt="${place.title}" class="place-image">
            <div class="place-content">
                <h2>${place.title}</h2>
                <p class="price">$${price} per night</p>
                <p>${place.description}</p>
                <p>Location: ${place.latitude}, ${place.longitude}</p>
                <div class="price-match"></div>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            </div>
        `;
        placesList.appendChild(placeCard);
    });

    const priceFilter = document.querySelector('.price-filter select');
    if (priceFilter) filterPlacesByPrice(priceFilter.value);
}

// ----------------------- PLACE DETAILS & REVIEWS -----------------------
async function fetchPlaceDetails(placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, { headers: { 'Content-Type': 'application/json' } });
        if (!response.ok) return showError('Failed to load place details');

        const place = await response.json();
        displayPlaceDetails(place);
    } catch (error) {
        console.error(error);
        showError('Error loading place details');
    }
}

function displayPlaceDetails(place) {
    const container = document.querySelector('.place-details');
    if (!container) return console.error('Place details container not found');

    container.innerHTML = '';

    const amenities = place.amenities.map(a => `<li>${a}</li>`).join('');

    container.innerHTML = `
        <h1>${place.title}</h1>
        <p>${place.description}</p>
        <p>Price: $${place.price} per night</p>
        <p>Location: ${place.latitude}, ${place.longitude}</p>
        <div class="amenities">
            <h3>Amenities:</h3>
            <ul>${amenities}</ul>
        </div>
    `;

    const token = getCookie('token');
    if (token) {
        const addReviewBtn = document.createElement('button');
        addReviewBtn.className = 'add-review-btn';
        addReviewBtn.textContent = 'Add Review';
        addReviewBtn.onclick = () => window.location.href = `/add_review.html?place_id=${place.id}`;
        container.appendChild(addReviewBtn);
    }
}

async function fetchReviews(placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/reviews/places/${placeId}/reviews`, { headers: { 'Content-Type': 'application/json' } });
        if (!response.ok) return showError('Failed to load reviews');

        const reviews = await response.json();
        displayReviews(reviews);
    } catch (error) {
        console.error(error);
        showError('Error loading reviews');
    }
}

function displayReviews(reviews) {
    const container = document.querySelector('.reviews-container');
    if (!container) return console.error('Reviews container not found');

    container.innerHTML = '<h2>Reviews</h2>';

    if (!reviews || reviews.length === 0) {
        container.innerHTML += '<p class="no-reviews">Aucun commentaire pour le moment. Soyez le premier à donner votre avis !</p>';
        return;
    }

    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        reviewCard.innerHTML = `
            <div class="review-user">${review.user_name || 'Anonymous'}</div>
            <div class="review-rating">Note: ${review.rating}/5</div>
            <p class="review-text">${review.text}</p>
            <small class="review-date">${new Date(review.created_at).toLocaleDateString()}</small>
        `;
        container.appendChild(reviewCard);
    });
}

// ----------------------- REVIEW FORM HANDLER -----------------------
async function handleReviewFormSubmit() {
    const placeId = new URLSearchParams(window.location.search).get('place_id');
    if (!placeId) return showError('Place ID not found');

    const rating = document.getElementById('rating').value;
    const text = document.getElementById('text').value;

    try {
        const response = await fetch(`http://localhost:5000/api/v1/reviews/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getCookie('token')}`
            },
            body: JSON.stringify({ text, rating: parseInt(rating), place_id: placeId })
        });

        if (response.ok) {
            window.location.href = `/place.html?id=${placeId}`;
        } else {
            const errorData = await response.json();
            showError(errorData.message || 'Failed to add review');
        }
    } catch {
        showError('Error adding review');
    }
}

// ----------------------- ERROR HANDLER -----------------------
function showError(message) {
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    document.querySelector('main')?.prepend(errorElement);
}
