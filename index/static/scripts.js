$(document).ready(function () {
    // Initially hide the modal and overlay
    $('#register_login').hide();
    $('#overlay').hide();

    // Function to show the modal and apply blur
    function showModal(isLogin) {
        $('#register_login').show();
        $('#overlay').show();
        $('#blurclass').addClass('blur');

        if (isLogin) {
            $('#login').show();
            $('#register').hide();
        } else {
            $('#register').show();
            $('#login').hide();
        }
    }

    // Function to hide the modal and remove blur
    function closeModal() {
        $('#register_login').hide();
        $('#overlay').hide();
        $('#blurclass').removeClass('blur');
    }

    // Show login form
    $('.login-btn').click(function (e) {
        e.preventDefault();
        showModal(true);
    });

    // Show register form
    $('.register-btn').click(function (e) {
        e.preventDefault();
        showModal(false);
    });

    // Close modal on close button or overlay click
    $('#close-modal, #overlay').click(function () {
        closeModal();
    });

    // Show job category if freelancer is selected
    $('#user-freelancer').change(function () {
        if ($(this).val() == 'freelancer') {
            $('#job-category').show();
        } else {
            $('#job-category').hide();
        }
    });
});

// Function to fetch freelancers (make sure it's in the global scope)
function fetchFreelancers(element) {
    const proid = element.getAttribute('data-proid');
    const url = `/freelancers?profession_id=${proid}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Handle the data, e.g., display it on the page
        })
        .catch(error => {
            console.error('Error fetching freelancers:', error);
        });
}
