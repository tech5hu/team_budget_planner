document.addEventListener('DOMContentLoaded', function() {
    const accountLink = document.querySelector('.account-link');
    const dropdown = document.querySelector('.account-dropdown');

    accountLink.addEventListener('click', function(event) {
        event.preventDefault();
        dropdown.classList.toggle('active');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
        if (!dropdown.contains(event.target) && !accountLink.contains(event.target)) {
            dropdown.classList.remove('active');
        }
    });
});
