document.addEventListener("DOMContentLoaded", () => {
    const animationDiv = document.getElementById("background-animation");
    const fadeInElements = document.querySelectorAll(".fade-in");

    // Ensure the background animation runs
    animationDiv.style.animation = "zoomOutBlur 1s ease forwards";

    // Wait for the background animation to complete 
    setTimeout(() => {
        // Hide the animation div after the animation completes
        animationDiv.classList.add("hidden");
        document.body.classList.remove("no-scroll"); // Allow scrolling

        // Add the 'visible' class to all fade-in elements
        fadeInElements.forEach((element) => {
            element.classList.add("visible");
        });
    }, 925);
});

function toggleSearchBar() {
    const bar = document.getElementById('searchForm');
    bar.classList.toggle('active');
}

function handleSearch(event) {
    event.preventDefault();
    const query = document.querySelector('.search-bar-container input[name="query"]').value;
    // Implement your search logic here (e.g., redirect or fetch results)
    alert('Searching for: ' + query);
}