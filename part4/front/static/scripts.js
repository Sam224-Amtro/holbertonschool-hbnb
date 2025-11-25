document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    setupLogout();
    setupPriceFilter();

    setupLoginForm();
    handlePlacePage();
    handleReviewForm();
});

/* -------------------------------------------------
   UTILITAIRES
--------------------------------------------------- */

function getCookie(name) {
    return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1];
}

function showError(message) {
    const container = document.querySelector('main');
    if (!container) return;

    const div = document.createElement('div');
    div.className = 'error-message';
    div.textContent = message;
    container.prepend(div);
}

/* -------------------------------------------------
   AUTHENTIFICATION
--------------------------------------------------- */

function checkAuthentication() {
    const token = getCookie('token');
    const nav = document.querySelector('.nav-links');
    const userProfile = document.querySelector('.user-profile');

    if (token) {
        fetchUserInfo(token);
        userProfile && (userProfile.style.display = 'flex');

        nav?.querySelectorAll('a[href="login.html"]')
            .forEach(a => a.style.display = 'none');
    } else {
        userProfile && (userProfile.style.display = 'none');
        nav?.querySelectorAll('a[href="login.html"]')
            .forEach(a => a.style.display = 'block');

        if (window.location.pathname.includes('add_review.html')) {
            window.location.href = 'login.html';
        }
    }
}

function setupLoginForm() {
    const form = document.querySelector('.form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = form.querySelector('input[type="email"]').value;
        const password = form.querySelector('input[type="password"]').value;
        await loginUser(email, password);
    });
}

async function loginUser(email, password) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            return showError(data.message || 'Login failed');
        }

        const expiry = new Date(Date.now() + 86400 * 1000).toUTCString();
        document.cookie = `token=${data.access_token}; expires=${expiry}; path=/; Secure; SameSite=Lax`;
        window.location.href = '/index.html';

    } catch {
        showError('Erreur de connexion au serveur');
    }
}

async function fetchUserInfo(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/users/me', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const user = await response.json();
            displayUserProfile(user);
        }
    } catch (e) {
        console.error('Error fetching user info:', e);
    }
}

function displayUserProfile(user) {
    const profile = document.querySelector('.user-profile');
    if (!profile) return;

    const name = profile.querySelector('.user-name');
    if (name) name.textContent = user.first_name;

    setupLogout();
}

function setupLogout() {
    document.querySelector('#logout-button')?.addEventListener('click', logout);
    document.querySelector('.logout-icon')?.addEventListener('click', logout);
}

function logout() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970; path=/;';
    window.location.href = 'index.html';
}

/* -------------------------------------------------
   PAGE "PLACE"
--------------------------------------------------- */

function handlePlacePage() {
    const isPlacePage = window.location.pathname.includes('place.html');
    const listPage = document.getElementById('places-list');

    if (isPlacePage) {
        const placeId = new URLSearchParams(window.location.search).get('id');
        if (!placeId) return showError('Place ID not found');

        fetchPlaceDetails(placeId);
        fetchReviews(placeId);

    } else if (listPage) {
        fetchPlaces();
    }
}

async function fetchPlaceDetails(placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`);
        if (!response.ok) return showError('Failed to load place details');

        const place = await response.json();
        displayPlaceDetails(place);
    } catch {
        showError('Error loading place details');
    }
}

function displayPlaceDetails(place) {
    const container = document.querySelector('.place-details');
    if (!container) return;

    container.innerHTML = `
        <h1>${place.title}</h1>
        <p>${place.description}</p>
        <p>Price: $${place.price} per night</p>
        <p>Location: ${place.latitude}, ${place.longitude}</p>
        <div class="amenities">
            <h3>Amenities:</h3>
            <ul>${place.amenities.map(a => `<li>${a}</li>`).join('')}</ul>
        </div>
    `;

    if (getCookie('token')) {
        const btn = document.createElement('button');
        btn.className = 'add-review-btn';
        btn.textContent = 'Add Review';
        btn.onclick = () => window.location.href = `/add_review.html?place_id=${place.id}`;
        container.appendChild(btn);
    }
}

/* -------------------------------------------------
   REVIEWS
--------------------------------------------------- */

function handleReviewForm() {
    const form = document.getElementById('reviewForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const placeId = new URLSearchParams(window.location.search).get('place_id');
        if (!placeId) return showError('Place ID not found');

        const rating = parseInt(document.getElementById('rating').value);
        const text = document.getElementById('text').value;

        try {
            const response = await fetch(`http://localhost:5000/api/v1/reviews/places/${placeId}/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('token')}`
                },
                body: JSON.stringify({ text, rating, place_id: placeId })
            });

            if (!response.ok) {
                const err = await response.json();
                return showError(err.message || 'Failed to add review');
            }

            window.location.href = `/place.html?id=${placeId}`;

        } catch {
            showError('Error adding review');
        }
    });
}

async function fetchReviews(placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/reviews/places/${placeId}/reviews`);
        if (!response.ok) return showError('Failed to load reviews');

        const reviews = await response.json();
        displayReviews(reviews);
    } catch {
        showError('Error loading reviews');
    }
}

function displayReviews(reviews) {
    const container = document.querySelector('.reviews-container');
    if (!container) return;

    container.innerHTML = '<h2>Reviews</h2>';

    if (!reviews.length) {
        container.innerHTML += `<p class="no-reviews">Aucun commentaire pour le moment.</p>`;
        return;
    }

    reviews.forEach(r => {
        const div = document.createElement('div');
        div.className = 'review-card';

        div.innerHTML = `
            <div class="review-user">${r.user_name || 'Anonymous'}</div>
            <div class="review-rating">Note: ${r.rating}/5</div>
            <p class="review-text">${r.text}</p>
            <small class="review-date">${new Date(r.created_at).toLocaleDateString()}</small>
        `;

        container.appendChild(div);
    });
}

/* -------------------------------------------------
   LISTE DES PLACES
--------------------------------------------------- */

const placeImages = [
    'https://images.unsplash.com/photo-1566073771259-6a8506099945?...',
    'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?...',
    'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?...',
    'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?...'
];

function getRandomPlaceImage() {
    return placeImages[Math.floor(Math.random() * placeImages.length)];
}

async function fetchPlaces() {
    const list = document.getElementById('places-list');
    if (!list) return;

    list.innerHTML = '<div class="loading">Loading places...</div>';

    try {
        const response = await fetch('http://localhost:5000/api/v1/places');
        if (!response.ok) throw new Error('Failed to fetch places');

        const places = await response.json();
        displayPlaces(places);

    } catch (error) {
        list.innerHTML = `<div class="error-message">${error.message}</div>`;
    }
}

function displayPlaces(places) {
    const list = document.getElementById('places-list');
    if (!list) return;

    list.innerHTML = places.map(place => `
        <div class="place-card">
            <img src="${getRandomPlaceImage()}" class="place-image">
            <div class="place-content">
                <h2>${place.title}</h2>
                <p class="price">$${place.price} per night</p>
                <p>${place.description}</p>
                <p>Location: ${place.latitude}, ${place.longitude}</p>
                <div class="price-match"></div>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            </div>
        </div>
    `).join('');

    const priceFilter = document.querySelector('.price-filter select');
    if (priceFilter) filterPlacesByPrice(priceFilter.value);
}

/* -------------------------------------------------
   FILTRE PRIX
--------------------------------------------------- */

function setupPriceFilter() {
    const select = document.querySelector('.price-filter select');
    if (!select) return;

    select.addEventListener('change', () => filterPlacesByPrice(select.value));
}

function filterPlacesByPrice(price) {
    const cards = document.querySelectorAll('.place-card');
    const container = document.querySelector('.price-filter');
    let hasVisible = false;

    container.querySelector('.no-results')?.remove();

    const msg = document.createElement('div');
    msg.className = 'no-results';
    msg.textContent = 'No places found for this price range';
    msg.style.display = 'none';
    container.appendChild(msg);

    cards.forEach(card => {
        const placePrice = parseInt(card.querySelector('.price').textContent.replace(/\D/g, ''));
        const info = card.querySelector('.price-match');

        card.style.display = 'none';
        info.textContent = '';

        if (price === 'all' || placePrice <= parseInt(price)) {
            card.style.display = 'block';

            if (price !== 'all') {
                info.textContent =
                    placePrice == price ? '✓ Exact price match' : `$${placePrice} (under budget)`;
                info.style.color = placePrice == price ? 'var(--secondary-color)' : 'var(--accent-color)';
            }

            hasVisible = true;
        }
    });

    msg.style.display = hasVisible ? 'none' : 'block';
}
