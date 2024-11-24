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

function fetchFreelancers(serviceBoxElement) {
    const professionId = serviceBoxElement.getAttribute('data-proid');
    
    if (!professionId) {
        console.error("Profession ID not found");
        return;
    }

    const url = `/freelancers/fetch/?profession_id=${professionId}`;
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                console.error(`HTTP error! status: ${response.status}`);
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                console.error("Error:", data.error);
            } else {
                // Redirect to the freelancer list page
                window.location.href = `/freelancers/?profession_id=${professionId}`;
            }
        })
        .catch(error => console.error("Error fetching freelancers:", error));
}




document.querySelector('form').addEventListener('submit', function(e) {
    var password = document.getElementById('password').value;
    var rePassword = document.getElementById('re_password').value;
    if (password !== rePassword) {
        e.preventDefault();
        alert('كلمات المرور غير متطابقة.');
    }
});

