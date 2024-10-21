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
const addMoreServiceBtn = document.getElementById('add-more-service');
const finalConfirmBtn = document.getElementById('final-confirm');
const selectDateBtn = document.getElementById('select-date');
const confirmDateTimeBtn = document.getElementById('confirm-date-time'); 
const confirmBookingBtn = document.getElementById('confirm-booking');
let isCardCentered = false;
let selectedServices = []; // Store multiple services with dates
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
    if (!calendar) {
        calendar = flatpickr('#datepicker', {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
            minDate: "today",
            onChange: function(selectedDates, dateStr, instance) {
                selectedTimeSlot = dateStr;  // Store selected date and time
                confirmDateTimeBtn.style.display = 'block';  // Show the button to confirm date and time
            }
        });
    }
}

// Move clicked card to center
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

    // Attach click event to each service item (menu item)
    const serviceItems = document.querySelectorAll('.service-item');
    serviceItems.forEach(item => {
        item.addEventListener('click', (event) => {
            event.preventDefault();
            selectedService = event.target.getAttribute('data-service');
            // Show the calendar popup and initialize the calendar
            showCalendarPopup();  // User selects date and time for this service
            initCalendar();  // Initialize the Flatpickr calendar
        });
    });
}

// Function to show the calendar popup
function showCalendarPopup() {
    calendarPopup.classList.add('show');  // Slide up the calendar
    calendarPopup.style.display = 'block';  // Ensure the popup is visible
    confirmDateTimeBtn.style.display = 'none'; // Initially hide the 'Confirm Date and Time' button
}

// Confirm the date and time selection by clicking 'Confirm Date and Time' button
confirmDateTimeBtn.addEventListener('click', () => {
    if (selectedTimeSlot) {
        // Hide the microservice menu
        microserviceMenu.style.display = 'none';

        // Hide the centered service card
        const activeCard = document.querySelector('.active-card');
        if (activeCard) {
            activeCard.style.display = 'none'; // Hide the centered card
            activeCard.classList.remove('active-card'); // Optionally remove the class
        }

        // Show the summary with selected service and time
        showSummary();
    }
});

// Function to show the summary after a service and date/time are selected
function showSummary() {
    // Add the selected service and time to the summary
    selectedServices.push({
        service: selectedService,
        timeSlot: selectedTimeSlot
    });

    // Clear existing summary details
    summaryDetails.innerHTML = '';

    // Generate the summary dynamically
    selectedServices.forEach((item, index) => {
        const summaryHTML = `
            <div class="summary-item">
                <i class="fas fa-concierge-bell"></i>
                <div>
                    <div class="summary-service">Service ${index + 1}: ${item.service}</div>
                    <div class="summary-date">Date: ${new Date(item.timeSlot).toLocaleDateString()}</div>
                    <div class="summary-time">Time: ${new Date(item.timeSlot).toLocaleTimeString()}</div>
                </div>
            </div>
        `;
        summaryDetails.innerHTML += summaryHTML;
    });

    // Ensure the booking summary is visible
    bookingSummary.style.display = 'block';

    // Hide the calendar popup and display the "Add More Service" and "Confirm Booking" buttons
    hideCalendarPopup();
    addMoreServiceBtn.style.display = 'block';
    finalConfirmBtn.style.display = 'block';
}

// Function to hide the calendar popup
function hideCalendarPopup() {
    calendarPopup.classList.remove('show');  // Slide down the calendar
    setTimeout(() => {
        calendarPopup.style.display = 'none';  // Completely hide after animation
    }, 500);  // Match the transition time in the CSS
}

// "Add More Service" button allows adding another service without resetting
addMoreServiceBtn.addEventListener('click', () => {
    // Allow user to add another service while keeping the existing summary
    microserviceMenu.style.display = 'none';
    calendarPopup.style.display = 'none'; // Hide any existing popup
    isCardCentered = false; // Allow the user to pick a new service
    document.querySelectorAll('.card').forEach(card => {
        card.style.display = 'block'; // Show all cards again
    });
});

// Final confirmation button to confirm all services and times
finalConfirmBtn.addEventListener('click', () => {
    const bookingNumber = generateBookingNumber();  // Generate a booking number
    alert(`Booking Confirmed! Your booking number is: ${bookingNumber}`);
    saveBookingHistory(bookingNumber);  // Save booking to the user's profile
});

// Function to generate a random booking number
function generateBookingNumber() {
    return 'BK' + Math.floor(Math.random() * 1000000);
}

// Function to save the booking history
function saveBookingHistory(bookingNumber) {
    // Assuming user profile is managed elsewhere, this will store the booking details
    const bookingHistory = {
        services: selectedServices,
        bookingNumber: bookingNumber,
        date: new Date().toLocaleString()
    };

    // Save booking to profile (this can be customized based on how you handle user profiles)
    console.log('Booking saved to profile:', bookingHistory);
    // Clear selected services after booking is confirmed
    selectedServices = [];
}