document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    setupLogout();
    setupPriceFilter();

  const loginForm = document.querySelector('.form');
  if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          const email = loginForm.querySelector('input[type="email"]').value;
          const password = loginForm.querySelector('input[type="password"]').value;
            await loginUser(email, password);
        });
    }

    // Vérifier si nous sommes sur la page place.html
    if (window.location.pathname.includes('place.html')) {
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');
        if (placeId) {
            fetchPlaceDetails(placeId);
            fetchReviews(placeId);
        } else {
            showError('Place ID not found');
        }
    } else if (document.getElementById('places-list')) {
        // Si nous sommes sur la page d'accueil, charger les lieux
        // Charger les lieux même si l'utilisateur n'est pas connecté
        fetchPlaces();
    }

    // Gestion du formulaire d'ajout de review
    const reviewForm = document.getElementById('reviewForm');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const placeId = new URLSearchParams(window.location.search).get('place_id');
            if (!placeId) {
                showError('Place ID not found');
                return;
            }

            const rating = document.getElementById('rating').value;
            const text = document.getElementById('text').value;

            try {
                const response = await fetch(`http://localhost:5000/api/v1/reviews/places/${placeId}/reviews`, {
                  method: 'POST',
                  headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${getCookie('token')}`
                    },
                    body: JSON.stringify({
                        text: text,
                        rating: parseInt(rating),
                        place_id: placeId
                    })
              });

              if (response.ok) {
                    // Rediriger vers la page du lieu
                    window.location.href = `/place.html?id=${placeId}`;
              } else {
                  const errorData = await response.json();
                    showError(errorData.message || 'Failed to add review');
              }
          } catch (error) {
                showError('Error adding review');
          }
      });
  }
});

// ----------------------- Authentification -----------------------

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function checkAuthentication() {
  const token = getCookie('token');
    const headerNav = document.querySelector('.header-nav');
    const navLinks = document.querySelector('.nav-links');
    const userProfile = document.querySelector('.user-profile');

  if (token) {
        // Récupérer les informations de l'utilisateur
        fetchUserInfo(token);

        // Afficher le profil utilisateur
        if (userProfile) {
            userProfile.style.display = 'flex';
        }

        // Cacher les liens de connexion
        if (navLinks) {
            const loginLinks = navLinks.querySelectorAll('a[href="login.html"]');
            loginLinks.forEach(link => link.style.display = 'none');
        }
  } else {
        // Cacher le profil utilisateur
        if (userProfile) {
            userProfile.style.display = 'none';
        }

        // Afficher les liens de connexion
        if (navLinks) {
            const loginLinks = navLinks.querySelectorAll('a[href="login.html"]');
            loginLinks.forEach(link => link.style.display = 'block');
        }

        // Rediriger vers login si sur une page protégée
        if (window.location.pathname.includes('add_review.html')) {
            window.location.href = 'login.html';
        }
    }
}

function createLogoutButton() {
    const btn = document.createElement('button');
    btn.id = 'logout-button';
    btn.className = 'logout-button';
    btn.textContent = 'Logout';
    document.querySelector('header')?.appendChild(btn);
    setupLogout();
    return btn;
}

function setupLogout() {
  const logoutButton = document.getElementById('logout-button');
  if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }

    const logoutIcon = document.querySelector('.logout-icon');
    if (logoutIcon) {
        logoutIcon.addEventListener('click', logout);
    }
}

function logout() {
    // Supprimer le cookie
          document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';

    // Rediriger vers la page d'accueil ou de connexion
          window.location.href = 'index.html';
}

async function loginUser(email, password) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            const date = new Date();
            date.setTime(date.getTime() + (24 * 60 * 60 * 1000));
            document.cookie = `token=${data.access_token}; expires=${date.toUTCString()}; path=/; Secure; SameSite=Lax`;
            window.location.href = '/index.html';
        } else {
            const errorData = await response.json();
            showError(errorData.message || 'Login failed');
        }
    } catch (error) {
        showError('Erreur de connexion au serveur');
    }
}

async function fetchUserInfo(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/users/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const user = await response.json();
            displayUserProfile(user);
        }
    } catch (error) {
        console.error('Error fetching user info:', error);
    }
}

function displayUserProfile(user) {
    const userProfile = document.querySelector('.user-profile');
    if (!userProfile) return;

    const name = userProfile.querySelector('.user-name');
    const logoutIcon = userProfile.querySelector('.logout-icon');

    if (name) {
        name.textContent = user.first_name;
    }
    setupLogout();
}

function setupPriceFilter() {
    const priceFilter = document.querySelector('.price-filter select');
    if (!priceFilter) return;

    priceFilter.addEventListener('change', (e) => {
        const selectedPrice = e.target.value;
        filterPlacesByPrice(selectedPrice);
    });
}

function filterPlacesByPrice(price) {
    const places = document.querySelectorAll('.place-card');
    const priceFilter = document.querySelector('.price-filter');
    let hasVisiblePlaces = false;

    // Supprimer l'ancien message s'il existe
    const oldMessage = priceFilter.querySelector('.no-results');
    if (oldMessage) {
        oldMessage.remove();
    }

    // Créer un nouveau message
    const noResults = document.createElement('div');
    noResults.className = 'no-results';
    noResults.textContent = 'No places found for this price range';
    noResults.style.display = 'none';
    priceFilter.appendChild(noResults);

    places.forEach(place => {
        const priceElement = place.querySelector('.price');
        if (!priceElement) return;

        const priceText = priceElement.textContent;
        const placePrice = parseInt(priceText.replace(/[^0-9]/g, ''));
        const priceMatch = place.querySelector('.price-match');

        if (price === 'all') {
            place.style.display = 'block';
            if (priceMatch) {
                priceMatch.textContent = '';
            }
            hasVisiblePlaces = true;
        } else {
            const selectedPrice = parseInt(price);
            if (placePrice <= selectedPrice) {
                place.style.display = 'block';
                if (priceMatch) {
                    if (placePrice === selectedPrice) {
                        priceMatch.textContent = '✓ Exact price match';
                        priceMatch.style.color = 'var(--secondary-color)';
                    } else {
                        priceMatch.textContent = `$${placePrice} (under budget)`;
                        priceMatch.style.color = 'var(--accent-color)';
                    }
                }
                hasVisiblePlaces = true;
            } else {
                place.style.display = 'none';
                if (priceMatch) {
                    priceMatch.textContent = '';
                }
            }
        }
    });

    // Afficher ou masquer le message "no results"
    noResults.style.display = hasVisiblePlaces ? 'none' : 'block';
}

// ----------------------- Place & Reviews -----------------------

async function fetchPlaceDetails(placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            showError('Failed to load place details');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Error loading place details');
    }
}

function displayPlaceDetails(place) {
    const detailsContainer = document.querySelector('.place-details');
    if (!detailsContainer) {
        console.error('Place details container not found');
        return;
    }

    // Vider le conteneur
    detailsContainer.innerHTML = '';

    // Créer et ajouter les éléments HTML
    const title = document.createElement('h1');
    title.textContent = place.title;

    const description = document.createElement('p');
    description.textContent = place.description;

    const price = document.createElement('p');
    price.textContent = `Price: $${place.price} per night`;

    const location = document.createElement('p');
    location.textContent = `Location: ${place.latitude}, ${place.longitude}`;

    const amenities = document.createElement('div');
    amenities.className = 'amenities';
    const amenitiesTitle = document.createElement('h3');
    amenitiesTitle.textContent = 'Amenities:';
    amenities.appendChild(amenitiesTitle);

    const amenitiesList = document.createElement('ul');
    place.amenities.forEach(amenity => {
        const li = document.createElement('li');
        li.textContent = amenity;
        amenitiesList.appendChild(li);
    });
    amenities.appendChild(amenitiesList);

    // Ajouter tous les éléments au conteneur
    detailsContainer.appendChild(title);
    detailsContainer.appendChild(description);
    detailsContainer.appendChild(price);
    detailsContainer.appendChild(location);
    detailsContainer.appendChild(amenities);

    // Ajouter le bouton pour ajouter une review si l'utilisateur est connecté
    const token = getCookie('token');
    if (token) {
        const addReviewBtn = document.createElement('button');
        addReviewBtn.className = 'add-review-btn';
        addReviewBtn.textContent = 'Add Review';
        addReviewBtn.onclick = () => {
            window.location.href = `/add_review.html?place_id=${place.id}`;
        };
        detailsContainer.appendChild(addReviewBtn);
    }
}

async function fetchReviews(placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/reviews/places/${placeId}/reviews`, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const reviews = await response.json();
            displayReviews(reviews);
        } else {
            showError('Failed to load reviews');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Error loading reviews');
    }
}

function displayReviews(reviews) {
    const reviewsContainer = document.querySelector('.reviews-container');
    if (!reviewsContainer) {
        console.error('Reviews container not found');
        return;
    }

    // Vider le conteneur
    reviewsContainer.innerHTML = '';

    // Ajouter le titre
    const title = document.createElement('h2');
    title.textContent = 'Reviews';
    reviewsContainer.appendChild(title);

    if (!reviews || reviews.length === 0) {
        const noReviews = document.createElement('p');
        noReviews.textContent = 'Aucun commentaire pour le moment. Soyez le premier à donner votre avis !';
        noReviews.className = 'no-reviews';
        reviewsContainer.appendChild(noReviews);
        return;
    }

    // Afficher les reviews
    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';

        const userInfo = document.createElement('div');
        userInfo.className = 'review-user';
        userInfo.textContent = review.user_name || 'Anonymous';

        const rating = document.createElement('div');
        rating.className = 'review-rating';
        rating.textContent = `Note: ${review.rating}/5`;

        const text = document.createElement('p');
        text.className = 'review-text';
        text.textContent = review.text;

        const date = document.createElement('small');
        date.className = 'review-date';
        date.textContent = new Date(review.created_at).toLocaleDateString();

        reviewCard.appendChild(userInfo);
        reviewCard.appendChild(rating);
        reviewCard.appendChild(text);
        reviewCard.appendChild(date);

        reviewsContainer.appendChild(reviewCard);
    });
}

// ----------------------- Places (Accueil) -----------------------

// Liste d'images aléatoires pour les lieux
const placeImages = [
    'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80',
    'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80',
    'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80',
    'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1473&q=80',
    'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80',
    'https://images.unsplash.com/photo-1560448204-603b3fc33ddc?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80',
    'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80',
    'https://images.unsplash.com/photo-1574362848149-11496d93a7c7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80'
];

// Fonction pour obtenir une image aléatoire
function getRandomPlaceImage() {
    const randomIndex = Math.floor(Math.random() * placeImages.length);
    return placeImages[randomIndex];
}

async function fetchPlaces(token = null) {
  const placesList = document.getElementById('places-list');
  if (!placesList) return;

  try {
      placesList.innerHTML = '<div class="loading">Loading places...</div>';

        // Préparer les headers
        const headers = {
              'Content-Type': 'application/json'
        };

        // Ajouter le token d'autorisation si disponible
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
          }

        const response = await fetch('http://localhost:5000/api/v1/places', {
            headers: headers
      });

      if (response.ok) {
          const places = await response.json();
          displayPlaces(places);
      } else {
          throw new Error('Failed to fetch places');
      }
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

    // Appliquer le filtre actuel après l'affichage des lieux
    const priceFilter = document.querySelector('.price-filter select');
    if (priceFilter) {
        filterPlacesByPrice(priceFilter.value);
    }
}

function showError(message) {
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    document.querySelector('main')?.prepend(errorElement);
}
