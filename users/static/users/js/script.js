// Set button text based on user role
document.addEventListener("DOMContentLoaded", function () {
    const userRole = "{{ user.role }}"; // Set dynamically in Django template
    const mainButton = document.getElementById("mainButton");

    if (userRole === "rocket_owner") {
        mainButton.textContent = "Rockets";
    } else {
        mainButton.textContent = "Cargo";
    }
});

// Toggle dropdown menu
function toggleDropdown() {
    document.getElementById("dropdownMenu").classList.toggle("show");
}

// Close dropdown if clicked outside
window.onclick = function (event) {
    if (!event.target.matches('.user-circle')) {
        let dropdowns = document.getElementsByClassName("dropdown-menu");
        for (let i = 0; i < dropdowns.length; i++) {
            let openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
};
