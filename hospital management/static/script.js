document.addEventListener('DOMContentLoaded', function () {
    // Background image transition logic
    let backgroundImages = document.querySelectorAll('.background-image');
    let currentIndex = 0;
  
    function showBackgroundImage() {
      backgroundImages[currentIndex].style.opacity = 1;
      currentIndex = (currentIndex + 1) % backgroundImages.length;
      setTimeout(showBackgroundImage, 3000);
    }
  
    showBackgroundImage();
  
    // Existing form validation for request appointment
    const requestAppointmentForm = document.querySelector(
      'form[action="/request_appointment"]'
    );
  
    if (requestAppointmentForm) {
      requestAppointmentForm.addEventListener('submit', function (event) {
        const doctorSelect = document.getElementById('doctor_id');
        const appointmentTime = document.getElementById('appointment_time');
  
        if (!doctorSelect.value) {
          alert('Please select a doctor.');
          event.preventDefault();
          return;
        }
  
        if (!appointmentTime.value) {
          alert('Please select a valid appointment time.');
          event.preventDefault();
          return;
        }
      });
    }
  
    // Example of confirmation before logout
    const logoutLinks = document.querySelectorAll('a[href="/logout"]');
  
    logoutLinks.forEach(link => {
      link.addEventListener('click', function (event) {
        const confirmLogout = confirm('Are you sure you want to log out?');
        if (!confirmLogout) {
          event.preventDefault();
        }
      });
    });
  
    // Example: Confirm navigation on unsaved changes
    const forms = document.querySelectorAll('form');
  
    forms.forEach(form => {
      form.addEventListener('change', function () {
        window.onbeforeunload = function () {
          return 'You have unsaved changes. Are you sure you want to leave?';
        };
      });
  
      form.addEventListener('submit', function () {
        window.onbeforeunload = null;
      });
    });
  
    // Example: Toggle visibility of error/success messages
    const flashMessages = document.querySelectorAll('.error, .success');
    flashMessages.forEach(message => {
      setTimeout(() => {
        message.style.opacity = 0;
        setTimeout(() => {
          message.style.display = 'none';
        }, 500);
      }, 3000); // Message disappears after 3 seconds
    });
  });
  