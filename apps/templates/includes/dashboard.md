# Soft UI Dashboard 

This is the Dashboard page for a web application built using the Soft UI design system. It provides an overview of key metrics, project statuses, and recent orders. 

## Features

* **Key Performance Indicators (KPIs)**: Visualizes important metrics like Today's Money, Users, New Clients, and Sales with clear percentage changes.
* **Charts**: Includes interactive charts using Chart.js to display:
    * Active Users (Bar Chart)
    * Sales Overview (Line Chart)
* **Projects Table**: Lists ongoing projects, showing the company, team members, budget, and completion progress.
* **Orders Timeline**: Provides a chronological view of recent order-related events.

## Technologies Used

* **Templating Engine:** Likely Jinja2 (based on `{{ }}` syntax) for creating dynamic HTML content.
* **CSS Framework:** Soft UI for styling and layout.
* **Charting Library:** Chart.js for data visualization.
* **JavaScript:** Used for chart rendering and possibly other interactive elements.

## Setup & Usage

* **Prerequisites:**
    * You'll need a web server and the required dependencies for the templating engine and Chart.js. 
    * The project structure suggests you'll need a `layouts` folder containing `base.html`, an `includes` folder with `footer.html`, and an `img` folder with the necessary images. 
* **Installation:**
    * Set up your web server and install any necessary dependencies. 
    * Place the provided code in the appropriate template file (e.g., `dashboard.html`). 
* **Configuration:**
    * Update `{{ config.ASSETS_ROOT }}` in the template to point to the correct location of your static assets (images, CSS, JS).
* **Running:**
    * Start your web server and navigate to the dashboard page.

## Customization

* **Data:** The current data for charts and tables is hardcoded. Connect the dashboard to a real data source (database, API) to make it dynamic.
* **Styling:** Customize the appearance using Soft UI's classes and variables. 
* **Functionality:** Add interactive features, filters, or more detailed views as needed for your application. 

**Note:** This README is based on the provided code snippet. A complete project would likely have additional setup instructions and more detailed documentation.

Let me know if you have any other questions or would like the README expanded upon as you develop the project further!