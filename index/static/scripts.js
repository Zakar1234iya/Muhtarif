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

    // // Close modal when clicking outside the content
    // $(document).mouseup(function (e) {
    //     var modalContent = $(".modal-content");
    //     if (!modalContent.is(e.target) && modalContent.has(e.target).length === 0) {
    //         closeModal();
    //     }
    // });
});
