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
    'nail-care': [
        'Pink & White Full Set - $60',
        'Pink & White Fill In - $50',
        'Acrylic Full Set - $50',
        'Acrylic Fill In - $40',
        'Gel Color Full Set - $50',
        'Gel Color Fill In - $40',
        'Dipping Powder - $50+',
        'UV Gel Full Set - $60',
        'UV Gel Fill In - $45',
        'Nail Repair - $5+',
        'Cut Down Designs - $5+'
    ],
    'manicure': [
        'Pedicure & Manicure - $50',
        'Regular Pedicure - $30',
        'Regular Manicure - $20',
        'Gel Manicure - $35',
        'Deluxe Manicure - $30',
        'Polish Change - $25+'
    ],
    'pedicure': ['Basic Pedicure - $35', 'Deluxe Pedicure - $50','Polish Change - $25+', 'Gel Pedicure - $45'],
    'waxing': [
        'Eyebrows - $10',
        'Chin - $8+',
        'Lip - $7',
        'Full Face - $30+',
        'Back - $45+',
        'Half Arms / Full Arms - $25+ / $35+',
        'Half Legs / Full Legs - $30+ / $40+',
        'Bikini - $40+'
    ]
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

// Function to show the microservice menu for the clicked service
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
    microserviceMenu.style.top = `${cardRect.bottom + window.scrollY + 20}px`; // Position 20px below the card
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

// "Add More Service" button allows adding another service without resetting
addMoreServiceBtn.addEventListener('click', () => {
    // Hide the booking summary temporarily
    bookingSummary.style.display = 'none';
    
    // Allow user to add another service while keeping the existing summary
    microserviceMenu.style.display = 'none';
    calendarPopup.style.display = 'none'; // Hide any existing popup

    // Reset card centering state
    isCardCentered = false; // Allow the user to pick a new service

    // Make all service cards visible again
    document.querySelectorAll('.card').forEach(card => {
        card.style.display = 'block'; // Show all cards again
    });

    // Scroll back to service card section if needed
    window.scrollTo({
        top: document.querySelector('.card-service-container').offsetTop,
        behavior: 'smooth'
    });
});


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

    // Save the booking information to localStorage
    const bookingInfo = {
        services: selectedServices,
        bookingNumber: bookingNumber,
        date: new Date().toLocaleString()
    };

    localStorage.setItem('latestBooking', JSON.stringify(bookingInfo));

    // Show an alert with booking number and redirect to profile
    alert(`Booking Confirmed! Your booking number is: ${bookingNumber}`);
    window.location.href = `/profile?bookingNumber=${bookingNumber}`;
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




//for profile page-----------------------


// Simulate user and booking data
 // Simulate user and booking data
 const user = {
    name: "Jane Doe",
    email: "jane.doe@example.com",
    phone: "123-456-7890",
    joinDate: "January 2023",
    gender: "female",  // Gender can be "male" or "female"
    bookings: [
        { service: "Basic Manicure", date: "2024-10-21", time: "10:30 AM", bookingNumber: "BK123456" },
        { service: "Full Body Wax", date: "2024-11-10", time: "2:00 PM", bookingNumber: "BK654321" }
    ]
};

// Populate user data
document.querySelector('.profile-header h1').textContent = `Welcome, ${user.name}!`;
document.querySelector('.details').innerHTML = `
    <h3>User Information</h3>
    <p><strong>Email:</strong> ${user.email}</p>
    <p><strong>Phone:</strong> ${user.phone}</p>
    <p><strong>Member Since:</strong> ${user.joinDate}</p>
`;

// Assign avatar based on gender
const avatarElement = document.getElementById('user-avatar');
if (user.gender === 'male') {
    avatarElement.src = 'https://via.placeholder.com/150?text=Male+Avatar';
} else {
    avatarElement.src = 'https://via.placeholder.com/150?text=Female+Avatar';
}

// Populate booking history
const bookingHistoryList = document.getElementById('booking-history-list');
user.bookings.forEach(booking => {
    const bookingItem = document.createElement('div');
    bookingItem.classList.add('booking-item');
    bookingItem.innerHTML = `
        <i class="fas fa-calendar-check"></i>
        <div class="booking-details">
            <p><strong>Service:</strong> ${booking.service}</p>
            <p><strong>Date:</strong> ${booking.date} at ${booking.time}</p>
            <p><strong>Booking Number:</strong> ${booking.bookingNumber}</p>
        </div>
    `;
    bookingHistoryList.appendChild(bookingItem);
});

// Logout functionality
document.querySelector('.btn-logout').addEventListener('click', () => {
    // Clear local storage or session data and redirect to login page
    localStorage.removeItem('authToken');
    window.location.href = '/login';
});

document.addEventListener('DOMContentLoaded', () => {
    // Retrieve the booking information from localStorage
    const bookingInfo = JSON.parse(localStorage.getItem('latestBooking'));

    // Check if there is a booking summary to display
    if (bookingInfo) {
        const bookingHistoryList = document.getElementById('booking-history-list');
        const summaryHTML = `
            <div class="booking-item">
                <i class="fas fa-calendar-check"></i>
                <div class="booking-details">
                    <p><strong>Booking Number:</strong> ${bookingInfo.bookingNumber}</p>
                    ${bookingInfo.services.map(service => `<p><strong>Service:</strong> ${service.service} at ${service.timeSlot}</p>`).join('')}
                    <p><strong>Booking Date:</strong> ${bookingInfo.date}</p>
                </div>
            </div>
        `;
        bookingHistoryList.innerHTML = summaryHTML;
    }
});
