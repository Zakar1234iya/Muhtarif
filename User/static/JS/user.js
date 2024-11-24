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