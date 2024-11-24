const profilePic = document.getElementById('profile-pic');
const iconsContainer = document.getElementById('icons-container');

profilePic.addEventListener('click', () => {
    if (iconsContainer.style.display === 'flex') {
        iconsContainer.style.display = 'none';
    } else {
        iconsContainer.style.display = 'flex';
    }
});

window.addEventListener('click', (e) => {
    if (!profilePic.contains(e.target) && !iconsContainer.contains(e.target)) {
        iconsContainer.style.display = 'none';
    }
});
// Hire freelancer logic (this can be further implemented in the backend)
function hireFreelancer(freelancerId) {
// Here you can use AJAX to send the freelancerId to the server for processing
alert("تم تعيين  الحرفي المحترف: " + freelancerId);
}