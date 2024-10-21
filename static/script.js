// Optional: Add JavaScript to control the gallery rotation speed or direction
document.addEventListener('DOMContentLoaded', function() {
    const gallery = document.querySelector('.gallery');
    let isPaused = false;

    gallery.addEventListener('mouseover', function() {
        gallery.style.animationPlayState = 'paused';
        isPaused = true;
    });

    gallery.addEventListener('mouseout', function() {
        gallery.style.animationPlayState = 'running';
        isPaused = false;
    });
});

//for login and logout handle
document.addEventListener('DOMContentLoaded', function() {
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    // Check if the user is logged in (e.g., check for a token in local storage)
    const isLoggedIn = localStorage.getItem('authToken') !== null;

    if (isLoggedIn) {
        loginLink.style.display = 'none';
        logoutLink.style.display = 'block';
    } else {
        loginLink.style.display = 'block';
        logoutLink.style.display = 'none';
    }

    // Handle logout
    logoutLink.addEventListener('click', function(event) {
        event.preventDefault();
        // Remove the token from local storage
        localStorage.removeItem('authToken');
        // Redirect to the login page
        window.location.href = '/login';
    });
});

/*document.addEventListener('DOMContentLoaded', function() {
    // Check if the user is logged in (e.g., check for a token in local storage)
    const isLoggedIn = localStorage.getItem('authToken') !== null;

    if (!isLoggedIn) {
        // Redirect to the login page if not logged in
        window.location.href = '/login';
    }
});*/

const cards = document.querySelectorAll('.card');
const microserviceMenu = document.getElementById('microservice-menu');
const microserviceList = document.getElementById('microservice-list');
const calendarPopup = document.getElementById('calendar-popup');
const bookingSummary = document.getElementById('booking-summary');
const summaryDetails = document.getElementById('summary-details');
const selectDateBtn = document.getElementById('select-date');
const confirmBookingBtn = document.getElementById('confirm-booking');
let isCardCentered = false;
let selectedService = '';
let selectedTimeSlot = '';

// Define the services for each main service
const serviceData = {
    'nail-care': ['Acrylic Nail - $25', 'Color Nail - $30', 'Polish Nail - $15'],
    'manicure': ['Basic Manicure - $20', 'French Manicure - $30'],
    'pedicure': ['Basic Pedicure - $35', 'Deluxe Pedicure - $50'],
    'waxing': ['Facial Wax - $20', 'Hand Wax - $25', 'Full Body Wax - $60', 'Bikini Wax - $45']
};

// Initialize Flatpickr for the calendar
let calendar = null; 
function initCalendar() {
    calendar = flatpickr('#datepicker', {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        minDate: "today",
        onChange: function(selectedDates, dateStr, instance) {
            selectedTimeSlot = dateStr;  // Store selected date and time
            // Enable the confirm booking button after date is selected
            confirmBookingBtn.style.display = 'block';
            selectDateBtn.style.display = 'none'; // Hide the select date button
        }
    });
}

cards.forEach(card => {
    card.addEventListener('click', () => {
        const service = card.getAttribute('data-service');

        if (!isCardCentered) {
            // First click: Move card to center
            cards.forEach(c => {
                if (c !== card) {
                    c.style.display = 'none';  // Hide other cards
                }
            });

            card.classList.add('active-card');
            isCardCentered = true;  // Mark the card as centered
        } else {
            // Second click: Show microservice menu based on the selected card
            showMicroserviceMenu(service, card);
        }
    });
});

// Function to display the microservice menu for the clicked service
function showMicroserviceMenu(service, card) {
    const services = serviceData[service];

    // Clear any existing services
    microserviceList.innerHTML = '';

    // Populate the list with the selected service's microservices
    services.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `<a href="#" class="service-item" data-service="${item}">${item}</a>`;
        microserviceList.appendChild(li);
    });

    // Position the menu below the card
    const cardRect = card.getBoundingClientRect();
    const menuWidth = microserviceMenu.offsetWidth;

    const cardCenterX = cardRect.left + (cardRect.width / 2);
    microserviceMenu.style.top = `${cardRect.bottom + window.scrollY + 20}px`; // 20px below the card
    microserviceMenu.style.left = `${cardCenterX - (menuWidth / 2)}px`;  // Center the menu below the card

    // Show the microservice menu
    microserviceMenu.style.display = 'block';

    // Attach click event to each service item for the calendar popup
    const serviceItems = document.querySelectorAll('.service-item');
    serviceItems.forEach(item => {
        item.addEventListener('click', (event) => {
            event.preventDefault();
            selectedService = event.target.getAttribute('data-service');
            // Show the calendar popup and initialize the calendar
            showCalendarPopup();
            initCalendar();  // Initialize the Flatpickr calendar
        });
    });
}

// Function to show calendar popup
function showCalendarPopup() {
    calendarPopup.classList.add('show');  // Slide up the calendar
    calendarPopup.style.display = 'block';  // Ensure the popup is visible
}

// Function to hide the calendar popup
function hideCalendarPopup() {
    calendarPopup.classList.remove('show');  // Slide down the calendar
    setTimeout(() => {
        calendarPopup.style.display = 'none';  // Completely hide after animation
    }, 500);  // Match the transition time in the CSS
}

// Confirm the time slot and show booking summary
confirmBookingBtn.addEventListener('click', () => {
    if (!selectedTimeSlot) {
        alert('Please select a date and time.');
        return;
    }

    // Hide the calendar popup
    hideCalendarPopup();

    // Show the booking summary
    showBookingSummary();
});

// Function to show the booking summary
function showBookingSummary() {
    summaryDetails.innerHTML = `
        <strong>Service:</strong> ${selectedService}<br>
        <strong>Time Slot:</strong> ${selectedTimeSlot}
    `;
    bookingSummary.classList.add('show');  // Show the summary
}






