// Chart.js for Energy Consumption Chart
const ctx = document.getElementById('energyChart').getContext('2d');
const energyChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'Energy Usage (kWh)',
            data: [10, 12, 9, 14, 16, 11],
            borderColor: '#4f46e5',
            backgroundColor: 'rgba(79, 70, 229, 0.3)',
            fill: true
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Dark Mode Toggle
const darkModeToggle = document.getElementById('darkModeToggle');
darkModeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
});

// Modal Functionality
const modal = document.getElementById('addDeviceModal');
const addDeviceBtn = document.getElementById('addDeviceBtn');
const cancelAddDevice = document.getElementById('cancelAddDevice');

addDeviceBtn.addEventListener('click', () => {
    modal.classList.add('show');
});

cancelAddDevice.addEventListener('click', () => {
    modal.classList.remove('show');
});

// Form Validation
const addDeviceForm = document.getElementById('addDeviceForm');
addDeviceForm.addEventListener('submit', function(event) {
    if (!this.checkValidity()) {
        event.preventDefault();
        alert('Please fill out all required fields.');
    }
});
