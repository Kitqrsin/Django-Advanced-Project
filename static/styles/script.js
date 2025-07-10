document.addEventListener("DOMContentLoaded", () => {
    const animationDiv = document.getElementById("background-animation");
    const fadeInElements = document.querySelectorAll(".fade-in");

    const hasVisited = localStorage.getItem("homeVisited");

    if (animationDiv && !hasVisited) {
        animationDiv.style.animation = "zoomOutBlur 1s ease forwards";
        setTimeout(() => {
            animationDiv.classList.add("hidden");
            document.body.classList.remove("no-scroll");
            fadeInElements.forEach((element) => {
                element.classList.add("visible");
            });

            localStorage.setItem("homeVisited", "true");
        }, 925);
    } else {

        fadeInElements.forEach((element) => {
            element.classList.add("visible");
        });
        if (animationDiv) {
            animationDiv.classList.add("hidden");
        }
        document.body.classList.remove("no-scroll");
    }

});

function toggleSearchBar() {
    const bar = document.getElementById('searchForm');
    bar.classList.toggle('active');
}

function handleSearch(event) {
    event.preventDefault();
    const query = document.querySelector('.search-bar-container input[name="query"]').value;
    window.location.href = `/search_query/?query=${encodeURIComponent(query)}`;

}

