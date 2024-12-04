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
let selectedServiceId = '';
let selectedTimeSlot = '';


document.addEventListener('DOMContentLoaded', function () {
    const usernameInput = document.getElementById('username');
    const usernameMsg = document.getElementById('username-msg');

    if (usernameInput) {
        usernameInput.addEventListener('input', function () {
            var username = this.value;

            // Make AJAX request to check username availability
            fetch('/check-username?username=' + username)
                .then(response => response.json())
                .then(data => {
                    if (data.username_taken) {
                        usernameMsg.innerText = "Username is already taken.";
                        usernameMsg.style.color = "red";
                    } else {
                        usernameMsg.innerText = "";
                    }
                });
        });
    }
});

function cancelBooking(apptId) {
    if (confirm("Are you sure you want to cancel this appointment?")) {
        fetch('/cancel_booking', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'appt_id=' + encodeURIComponent(apptId)
        })
        .then(response => {
            if (!response.ok) {
                // Handle HTTP errors
                return response.json().then(data => {
                    throw new Error(data.error || 'An error occurred.');
                });
            }
            return response.json();
        })
        .then(data => {
            alert(data.success || 'Booking canceled successfully');
            location.reload(); // Reload the page to update appointment list
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message || 'An error occurred. Please try again.');
        });
    }
}



let calendar = null;

function initCalendar() {
    const employeeSchedule = [0, 1, 1, 1, 1, 1, 1]; // Sunday to Saturday schedule (0: off, 1: on)

    if (!calendar) {
        const now = new Date();
        const maxDate = new Date();
        maxDate.setDate(now.getDate() + 14);

        calendar = flatpickr('#datepicker', {
            enableTime: true,
            dateFormat: "m/d/Y h:i:S K",
            minDate: now,
            maxDate: maxDate,
            minuteIncrement: 30,


            enable: [
                function(date) {
                    
                    const day = date.getDay();
                    
                    return employeeSchedule[day] === 1;
                }
            ],

            onChange: function(selectedDates, dateStr, instance) {
                selectedTimeSlot = dateStr; 
                confirmDateTimeBtn.style.display = 'block';  
            }
        });
    }
}

// Call fetchServiceData once when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchServiceData().then(() => {
        showMicroserviceMenu(serviceType, cardElement);
    });
});



let serviceData = {};
function fetchServiceData() {
    return fetch('/get_services') 
        .then(response => response.json())
        .then(data => {
            serviceData = data;
        })
        .catch(error => console.error('Error fetching service data:', error));
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




// Function to show microservice menu for a selected service type
function showMicroserviceMenu(service, card) {
    const services = serviceData[service];

    if (!services) {
        console.error(`No services found for type: ${service}`);
        return;
    }

    // Clear any existing services
    microserviceList.innerHTML = '';

    // Populate the list with the selected service's microservices
    services.forEach(item => {
        const li = document.createElement('li');
        // Include service_id as a data attribute for future use
        li.innerHTML = `<a href="#" class="service-item" data-service-id="${item.service_id}" data-service="${item.service_name}">${item.service_name}</a>`;
        microserviceList.appendChild(li);
    });

    // Show the microservice menu
    microserviceMenu.style.display = 'block';

    // Attach click event to each service item
    const serviceItems = document.querySelectorAll('.service-item');
    serviceItems.forEach(item => {
        item.addEventListener('click', (event) => {
            event.preventDefault();
             selectedService = event.target.getAttribute('data-service');
             selectedServiceId = event.target.getAttribute('data-service-id');
            showCalendarPopup();
            initCalendar();
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
        service_id: selectedServiceId,
        service: selectedService,
        timeSlot: selectedTimeSlot
    });

    // Clear existing summary details
    summaryDetails.innerHTML = '';

    // Generate the summary dynamically
    selectedServices.forEach((item, index) => {
        const date = new Date(item.timeSlot);

        const summaryHTML = `
            <div class="summary-item">
                <i class="fas fa-concierge-bell"></i>
                <div>
                    <div class="summary-service">Service ${index + 1}: ${item.service}</div>
                    <div class="summary-service">Service ID: ${item.service_id}</div>
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
    }, 500);
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
    const bookingNumber = generateBookingNumber();

    // Save the booking information
    const bookingInfo = {
        services: selectedServices,
        bookingNumber: bookingNumber,
        date: new Date().toLocaleString()
    };

    // Send the data to the Flask backend using POST request
    fetch('/final-confirm', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookingInfo)
    })
    .then(response => response.json())
    .then(data => {
        // Show an alert with the booking number and then redirect
        alert(`Booking Confirmed! Your booking number is: ${bookingNumber}`);
        window.location.href = `/profile?bookingNumber=${bookingNumber}`;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});


// Function to generate a random booking number
function generateBookingNumber() {
    return 'BK' + Math.floor(Math.random() * 1000000);
}



//seller side =========================================================


//============================seller side================================


    document.addEventListener("DOMContentLoaded", function() {
        document.querySelectorAll("form[id^='addServiceForm']").forEach((form) => {
            form.addEventListener("submit", addService);
        });
    });

    async function addService(event) {
        event.preventDefault();
    
        const form = event.target.closest('form');
        const category = form.id.split("-")[1];
        const table = document.querySelector(`#${category}-table tbody`);
    
        if (!table) {
            console.error(`Table for category "${category}" not found.`);
            return;
        }
    
        const serviceName = form.querySelector(`input[id$='ServiceName-${category}']`).value;
        const servicePrice = form.querySelector(`input[id$='ServicePrice-${category}']`).value;
        const serviceImageInput = form.querySelector(`input[id$='ServiceImage-${category}']`);
        if (serviceImageInput.files.length === 0) {
            alert("Please select an image for the new service.");
            return;
        }
    
        const formData = new FormData();
        formData.append("type", category);
        formData.append("service_image", serviceImageInput.files[0]);
        formData.append("service_name", serviceName);
        formData.append("service_price", servicePrice);
    
        const response = await fetch('/add-service', {
            method: 'POST',
            body: formData
        });
        

        const result = await response.json();
    
        if (response.ok) {
            location.reload();
            // Reset form fields after adding service
            form.querySelector(`input[id$='ServiceName-${category}']`).value = '';
            form.querySelector(`input[id$='ServicePrice-${category}']`).value = '';
            serviceImageInput.value = '';
        } else {
            alert("Failed to upload image: " + result.error);
        }
    }
    


    async function editService(button) {
        const row = button.closest('tr');
        const serviceNameCell = row.cells[0];
        const serviceImageCell = row.cells[1];
        const servicePriceCell = row.cells[2];
        const serviceID = button.getAttribute('data-service-id');
        const category = button.getAttribute('data-service-type');
        let image_changed = false;
        
        if (button.textContent === 'Save') {
            const newName = serviceNameCell.querySelector('input').value;
            const newPrice = servicePriceCell.querySelector('input').value;
            const newImageFile = serviceImageCell.querySelector('input[type="file"]').files[0];

            serviceNameCell.textContent = newName;
            servicePriceCell.textContent = `$${newPrice}`;

            const formData = new FormData();
        
            if (newImageFile) {
                formData.append("service_image", newImageFile);
                image_changed = true;
            }
            formData.append("type", category);
            formData.append("service_name", newName);
            formData.append("service_price", newPrice);
            formData.append("id", serviceID);
            formData.append("image_changed", image_changed.toString());
            console.log(category, newName, newPrice,serviceID, image_changed);
        
            // Upload image to the server
            const response = await fetch('/update-service', {
                method: 'POST',
                body: formData
            });
            

            const result = await response.json();
        
            if (response.ok) {
                location.reload();
            } else {
                alert("Failed to upload image: " + result.error);
            }

            button.textContent = 'Edit';
        } else {
            const currentName = serviceNameCell.textContent;
            const currentPrice = servicePriceCell.textContent.replace('$', '');
            const currentImageURL = serviceImageCell.querySelector('img').src;

            serviceNameCell.innerHTML = `<input type="text" value="${currentName}" class="form-control">`;
            servicePriceCell.innerHTML = `<input type="number" value="${currentPrice}" class="form-control">`;
            serviceImageCell.innerHTML = `
                <img src="${currentImageURL}" alt="${currentName}" style="width: 80px; height: 60px; display:block; margin-bottom: 10px;">
                <input type="file" class="form-control" style="width: 80px; font-size: 12px;">
            `;

            button.textContent = 'Save';
        }
    }

    async function removeService(button) {
        if (confirm("Are you sure you want to remove this service?")) {
            const row = button.closest('tr');
            const serviceID = button.getAttribute('data-service-id');

            const response = await fetch('/remove-service', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(serviceID),
            });
            const result = await response.json();

            if (response.ok) {
                location.reload();
            } else {
                alert("Failed to upload image: " + result.error);
            }
        }
    }


    // employee edit and delete

    document.addEventListener("DOMContentLoaded", function() {
        // Add event listeners for edit and delete buttons
        document.querySelectorAll(".edit-button-employee").forEach(button => {
            button.addEventListener("click", editEmployee);
        });

        document.querySelectorAll(".delete-button-employee").forEach(button => {
            button.addEventListener("click", deleteEmployee);
        });
    });

    // Function to handle editing employee details
    function editEmployee(event) {
        const employeeBox = event.target.closest(".employee-info-box");
        const infoDiv = employeeBox.querySelector("#employee-info");

        if (event.target.textContent === "Edit") {
            // Switch to edit mode
            infoDiv.innerHTML = `
                <h5>Name: <input type="text" value="${employeeBox.getAttribute('data-name')}" class="form-control" id="edit-name"></h5>
                <h5>Employee ID: <input type="text" value="123456" class="form-control" id="edit-id" disabled></h5>
                <h5>Position: <input type="text" value="Nail Technician" class="form-control" id="edit-position"></h5>
                <h5>Phone Number: <input type="text" value="${employeeBox.getAttribute('data-phone')}" class="form-control" id="edit-phone"></h5>
                <h5>Email: <input type="email" value="abc@gmail.com" class="form-control" id="edit-email"></h5>
                <h5>Upload New Picture: <input type="file" class="form-control" id="edit-picture"></h5>
            `;
            event.target.textContent = "Save";
        } else {
            // Save changes
            const name = document.getElementById("edit-name").value;
            const position = document.getElementById("edit-position").value;
            const phone = document.getElementById("edit-phone").value;
            const email = document.getElementById("edit-email").value;

            // Update the display with new data
            infoDiv.innerHTML = `
                <h5>Name: [ ${name} ]</h5>
                <h5>Employee ID: [ 123456 ]</h5>
                <h5>Position: [ ${position} ]</h5>
                <h5>Phone Number: [ ${phone} ]</h5>
                <h5>Email: [ ${email} ]</h5>
            `;

            // Update data attributes for future reference
            employeeBox.setAttribute('data-name', name);
            employeeBox.setAttribute('data-phone', phone);

            // Change button text back to "Edit"
            event.target.textContent = "Edit";
        }
    }

    // Function to handle deleting an employee
    function deleteEmployee(event) {
        const employeeBox = event.target.closest(".employee-info-box");
        employeeBox.remove();
    }

    function confirmCancel() {
        if (confirm("Are you sure you want to mark this appointment as a no-show?")) {
            // Submit the form if confirmed
            document.querySelector('#cancel-booking form').submit();
        }
    }




    //==========employee editing===========

    document.addEventListener("DOMContentLoaded", function () {
        // Bind form submission to add new employee
        document.getElementById("addEmployeeForm-editemp").addEventListener("submit", addEmployee);
    });

    function addEmployee(event) {
        event.preventDefault();

        // Get form values
        const name = document.getElementById("newEmployeeName-editemp").value;
        const phone = document.getElementById("newEmployeePhone-editemp").value;
        const expertise = document.getElementById("newEmployeePosition-editemp").value;
        const email = document.getElementById("newEmployeeEmail-editemp").value;

        const newEmployee = {
            name: name,
            phone: phone,
            expertise: expertise,
            email: email
        };

        fetch('/add-employee', {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify(newEmployee)
        })
        .then(response => response.json())
        .then(data => {
            if(data.success){
                alert('Employee added successsfully')
                location.reload()
            }
            else{
                alert(data.error || 'Something went wrong')
            }
        })
        .catch(error => {
          console.error('Error', error)
          alert(data.error || 'Something went wrong, please try again')      
        });

        // Clear input fields after adding employee
        document.getElementById("newEmployeeName-editemp").value = '';
        document.getElementById("newEmployeePhone-editemp").value = '';
        document.getElementById("newEmployeePosition-editemp").value = '';
        document.getElementById("newEmployeeEmail-editemp").value = '';
    }

    function editEmp(button) {
        const row = button.closest("tr");
        // const cells = row.getElementsByTagName("td");
        const cells = row.querySelectorAll('td:not(:first-child):not(:last-child)');
        const employeeID = row.querySelector('td:first-child').textContent.trim()
        if (button.textContent === "Save") {
            // Save edited values
            const newName = cells[0].querySelector("input").value;
            const newPhone = cells[1].querySelector("input").value;
            const newPosition = cells[2].querySelector("input").value;
            const newEmail = cells[3].querySelector("input").value;

            // Set updated values to cells
            cells[0].textContent = newName;
            cells[1].textContent = newPhone;
            cells[2].textContent = newPosition;
            cells[3].textContent = newEmail;
            const dataToSend = {
                name: newName,
                phone: newPhone,
                expertise: newPosition,
                email: newEmail,
                id: employeeID
            };

            fetch('/edit-employee-info',
                {
                    method: 'POST',
                    headers: {'content-type': 'application/json'},
                body: JSON.stringify(dataToSend)
                })
                .then(response => response.json())
                .then(data => {
                    if(data.success){

                    }
                    else{
                        alert(data.error || 'An error has occured')
                    }
                })
                .catch(error => {
                    console.error('Error', error),
                    alert(data.error || 'An Error has occured, please try again')
                });

            button.textContent = "Edit";
        } else {
            // Switch to edit mode by creating input fields
            const currentName = cells[0].textContent.trim();
            const currentPhone = cells[1].textContent.trim();
            const currentPosition = cells[2].textContent.trim();
            const currentEmail = cells[3].textContent.trim();

            cells[0].innerHTML = `<input type="text" value="${currentName}" class="form-control">`;
            cells[1].innerHTML = `<input type="text" value="${currentPhone}" class="form-control">`;
            cells[2].innerHTML = `<input type="text" value="${currentPosition}" class="form-control">`;
            cells[3].innerHTML = `<input type="text" value="${currentEmail}" class="form-control">`;

            button.textContent = "Save";

        }
    }

    function editManager(button) {
        const row = button.closest("tr");
        // const cells = row.getElementsByTagName("td");
        const cells = row.querySelectorAll('td:not(:first-child):not(:last-child)');
        const managerID = row.querySelector('td:first-child').textContent.trim()
        if (button.textContent === "Save") {
            // Save edited values
            const newName = cells[0].querySelector("input").value;
            const newPhone = cells[1].querySelector("input").value;
            const newEmail = cells[2].querySelector("input").value;

            // Set updated values to cells
            cells[0].textContent = newName;
            cells[1].textContent = newPhone;
            cells[2].textContent = newEmail;
            const dataToSend = {
                name: newName,
                phone: newPhone,
                email: newEmail,
                id: managerID
            };
            console.log(dataToSend);

            fetch('/edit-manager-info',
                {
                    method: 'POST',
                    headers: {'content-type': 'application/json'},
                body: JSON.stringify(dataToSend)
                })
                .then(response => response.json())
                .then(data => {
                    if(data.success){

                    }
                    else{
                        alert(data.error || 'An error has occured')
                    }
                })
                .catch(error => {
                    console.error('Error', error),
                    alert(data.error || 'An Error has occured, please try again')
                });

            button.textContent = "Edit";
        } else {
            // Switch to edit mode by creating input fields
            const currentName = cells[0].textContent.trim();
            const currentPhone = cells[1].textContent.trim();
            const currentPosition = cells[2].textContent.trim();

            cells[0].innerHTML = `<input type="text" value="${currentName}" class="form-control">`;
            cells[1].innerHTML = `<input type="text" value="${currentPhone}" class="form-control">`;
            cells[2].innerHTML = `<input type="text" value="${currentPosition}" class="form-control">`;

            button.textContent = "Save";

        }
    }

    function removeEmp(button) {
        if (confirm("Are you sure you want to remove this employee?")) {
            const row = button.closest("tr");
            const employeeID = row.querySelector('td:first-child').textContent.trim();
            // row.remove();
            fetch('/remove-employee', {
                method: 'POST',
                headers: {
                    'content-type': 'application/json'
                },
                body: JSON.stringify({employeeID})
            })
            .then(response => response.json())
            .then(data => {
                if(data.success){
                    alert('Employee removed successfully')
                    row.remove();
                }
                else{
                    console.error('Error', error);
                    alert(data.error || 'An error has occured')
                }
            })
            .catch(error => {
                console.error('Error', error),
                alert(data.error || 'An error has occured, pleast try again')
            });
        }
        else{
            alert("something went wrong")
            console.log('something went wrong', employeeID)
        }
    }

    function removeManager(button) {
        if (confirm("Are you sure you want to remove this manager?")) {
            const row = button.closest("tr");
            const employeeID = row.querySelector('td:first-child').textContent.trim();

            fetch('/remove-manager', {
                method: 'POST',
                headers: {
                    'content-type': 'application/json'
                },
                body: JSON.stringify({employeeID})
            })
            .then(response => response.json())
            .then(data => {
                if(data.success){
                    alert('Manager removed successfully')
                    row.remove();
                }
                else{
                    alert(data.error || 'An error has occured')
                }
            })
            .catch(error => {
                console.error('Error', error),
                alert(data.error || 'An error has occured, pleast try again')
            });
        }
        else{
            alert("something went wrong")
            console.log('something went wrong', employeeID)
        }
    }

    //=======edit store timing======
    function editTime(button) {
        const row = button.closest("tr");
        const current_day = row.querySelector('td:first-child').textContent.trim();
        const openCell = row.cells[1]; 
        const closeCell = row.cells[2]; 
        
        if (button.textContent === "Edit") {
            // Get the current time values in 12-hour format
            const currentOpen = to12HourFormat(openCell.textContent.trim());
            const currentClose = to12HourFormat(closeCell.textContent.trim());

            // Replace text content with input fields
            openCell.innerHTML = `<input type="time" value="${to24HourFormat(currentOpen)}" class="form-control">`;
            closeCell.innerHTML = `<input type="time" value="${to24HourFormat(currentClose)}" class="form-control">`;

            button.textContent = "Save";
        } else {
            // Retrieve values in 24-hour format and convert them to 12-hour format for display
            const newOpen = openCell.querySelector("input").value;
            const newClose = closeCell.querySelector("input").value;

            const hours = {
                day: current_day,
                open: newOpen,
                close: newClose
            };
            console.log(hours);

            openCell.textContent = to12HourFormat(newOpen);
            closeCell.textContent = to12HourFormat(newClose);

            button.textContent = "Edit";

        fetch('/change-store-hours', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(hours)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                
            } else {
                alert(data.error || 'An error occurred.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
        }

    }

    // Function to convert 24-hour time to 12-hour format
    function to12HourFormat(time) {
        const [hours, minutes] = time.split(":");
        const period = hours >= 12 ? "PM" : "AM";
        const adjustedHours = hours % 12 || 12; 
        return `${adjustedHours}:${minutes} ${period}`;
    }

    // Function to convert 12-hour time to 24-hour format (for input field compatibility)
    function to24HourFormat(time) {
        const [timePart, period] = time.split(" ");
        let [hours, minutes] = timePart.split(":");
        if (period === "PM" && hours !== "12") hours = parseInt(hours) + 12;
        if (period === "AM" && hours === "12") hours = "00";
        return `${hours}:${minutes}`;
    }




    //===========scheudle edit =========

   //===========schedule edit =========
   function editSch(button) {
    const row = button.closest('tr');
    const cells = row.querySelectorAll('td:not(:first-child):not(:nth-child(2)):not(:last-child)');
    const timeSlotCell = row.querySelector('td:nth-child(2)');
    
    // Log to check what content is retrieved
    console.log("Time Slot Cell:", timeSlotCell);

    const timeSlot = timeSlotCell ? timeSlotCell.textContent.trim() : ""; // Get time slot, safely checking for existence

    // Extract managerID from the managerInfo string (e.g., "John Doe ID:101123")


    if (button.textContent === 'Edit') {
        cells.forEach(cell => {
            const currentText = cell.textContent;
            cell.innerHTML = `<input type="text" value="${currentText}" class="small-input" />`;
        });
        button.textContent = 'Save';
    } else {
        // Collect the data to send to the server
        const dataToSend = {timeSlot, days: {} };

        cells.forEach((cell, index) => {
            const dayName = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'][index];
            const input = cell.querySelector('input');
            if (input) {
                cell.textContent = input.value; // Set cell text to input value
                dataToSend.days[dayName] = input.value; // Add to data object
            }
        });
    console.log("Time Slot:", timeSlot); // Log the time slot value to see what's being retrieved
    console.log("Data to send:", dataToSend);
        button.textContent = 'Edit';

        // Send data to server with fetch
        fetch('/save-week-schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataToSend) // Send structured data
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // alert(data.success);
                // Reload the profile page to reflect updated schedule
                location.reload();
            } else {
                alert(data.error || 'An error occurred.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }



    //===========search employee =========

   //===========search employee=========
    function searchEmp(){
        const user_input = document.getElementById('search-employee').value().trim();

        
        fetch('/search-employee', {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify(user_input)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert(data.error, 'Something Went wrong');
            }
        })
        .catch(error => {
            console.log('Error:', error);
            alert('An error occured, please try again');
        });
    }

}

script.js
