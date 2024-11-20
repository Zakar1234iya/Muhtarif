$(document).ready(function () {
    // Initially hide the modal
    $('#register_login').hide();
    $('#overlay').hide();

    // Show the login form when the login button is clicked
    $('.login-btn').click(function (e) {
        e.preventDefault(); // Prevent the default action of the link
        $('#register_login').show(); // Show the modal
        $('#overlay').show(); // Show the dark overlay
        $('#register').hide(); // Hide the register form
        $('#login').show(); // Show the login form
        $('body').addClass('blur'); // Apply the blur effect to the background content
    });

    // Show the register form when the register button is clicked
    $('.register-btn').click(function (e) {
        e.preventDefault(); // Prevent the default action of the link
        $('#register_login').show(); // Show the modal
        $('#overlay').show(); // Show the dark overlay
        $('#login').hide(); // Hide the login form
        $('#register').show(); // Show the register form
        $('body').addClass('blur'); // Apply the blur effect to the background content
    });

    // Close the modal when the close button is clicked
    $('#close-modal').click(function (e) {
        e.preventDefault(); // Prevent the default action
        $('#register_login').hide(); // Hide the modal
        $('#overlay').hide(); // Hide the dark overlay
        $('body').removeClass('blur'); // Remove the blur effect from the page
    });

    // Close the modal when the overlay is clicked
    $('#overlay').click(function () {
        $('#register_login').hide(); // Hide the modal
        $('#overlay').hide(); // Hide the dark overlay
        $('body').removeClass('blur'); // Remove the blur effect from the page
    });
});
