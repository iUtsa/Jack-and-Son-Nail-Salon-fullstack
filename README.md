# 🌸 Jack and Son Nails Spa 🌸

![License](https://img.shields.io/badge/license-MIT-blue)
![Made with Flask](https://img.shields.io/badge/Backend-Flask-blue)
![Frontend with Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap-orange)
![Database](https://img.shields.io/badge/Database-MySQL-green)

Jack and Son Nails Spa is a scheduling and employee management system designed to streamline salon operations. This application allows you to manage employee shifts, client bookings, and view schedules in a colorful, easy-to-navigate interface.

---

## 🚀 Features

Click on each feature for details:

| Feature                 | Description                                                            |
|-------------------------|------------------------------------------------------------------------|
| **Employee Management** | <span onclick="toggleDetails('employee')">➤ Add, edit, and remove employees with essential details.</span> |
| **Shift Scheduling**    | <span onclick="toggleDetails('shift')">➤ Assign shifts to employees with unique color-coded blocks per slot.</span> |
| **Client Booking**      | <span onclick="toggleDetails('booking')">➤ Clients can view and book based on available time slots.</span> |
| **Responsive Layout**   | <span onclick="toggleDetails('layout')">➤ Works smoothly on any device, adapting to different screen sizes.</span> |

<div id="employee" style="display: none;">
  - **Employee Management**: Quickly add, modify, and remove employee records, storing essential details and availability.
</div>

<div id="shift" style="display: none;">
  - **Shift Scheduling**: Assign shifts with unique color codes, ensuring clear visibility of availability.
</div>

<div id="booking" style="display: none;">
  - **Client Booking**: Clients can easily book based on available slots, enhancing appointment management.
</div>

<div id="layout" style="display: none;">
  - **Responsive Layout**: Fully responsive, ensuring seamless experience on mobile, tablet, and desktop.
</div>

---

## 📂 Project Structure

- **Frontend**: ![HTML5](https://img.icons8.com/color/48/000000/html-5.png) ![CSS3](https://img.icons8.com/color/48/000000/css3.png) ![JavaScript](https://img.icons8.com/color/48/000000/javascript.png) - UI, forms, and real-time interactions
- **Backend**: ![Flask](https://img.icons8.com/ios-filled/48/000000/flask.png) - Flask for server requests, scheduling logic, and data persistence
- **Styling**: ![Bootstrap](https://img.icons8.com/color/48/000000/bootstrap.png) - Clean, responsive design for intuitive navigation
- **Database**: ![MySQL](https://img.icons8.com/color/48/000000/mysql-logo.png) - MySQL for backend efficiency and secure data management

---

## 🔧 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/jack-and-son-nails-spa.git
cd jack-and-son-nails-spa
2. Set Up the Environment
Ensure you have Python installed.
Create and activate a virtual environment:
bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Run the Application
bash
Copy code
flask run
5. Access the Application
Open localhost to view in your browser.

💻 Usage
Employee Management: Go to the Employee page to add or modify employee details.
Scheduling: Assign employees to specific shifts and adjust time ranges as needed.
Booking: Clients book slots based on employee availability shown on the booking calendar.
🤝 Contributing
Contributions are welcome! Please fork the repo, make changes, and submit a pull request.

Enjoy managing your salon with ease!

<script> function toggleDetails(id) { var element = document.getElementById(id); if (element.style.display === "none") { element.style.display = "block"; } else { element.style.display = "none"; } } </script>
vbnet
Copy code

### Explanation of Enhancements

1. **Feature Toggles**: The JavaScript function `toggleDetails` allows users to click on each feature's name to expand and view additional details interactively.
2. **Technology Icons**: Icons are added for each technology, providing a visual indicator of the tech stack.
3. **Shields and Labels**: Additional badges highlight tools and frameworks.
4. **Dynamic Interaction**: The JavaScript script enables information toggling directly in the README. 

**Note**: JavaScript won’t run on GitHub’s markdown rendering directly. To achieve this effect live, you’d need to host this markdown on your website or use a GitHub Pages site. However, for a simple README, you may consider replacing the toggle details with simple expandable sections using markdown details syntax, like:

```markdown
<details>
  <summary>Employee Management</summary>
  - Quickly add, modify, and remove employee records, storing essential details and availability.
</details>
