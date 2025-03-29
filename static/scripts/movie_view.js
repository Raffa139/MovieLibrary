const handleMovieViewMode = () => {
    const viewModeInput = document.querySelector("#movie-view");

    if (viewModeInput) {
        const changeClass = (movie, newClass) => {
            ["compact", "normal", "wide"].forEach(e => movie.classList.remove(e));
            movie.classList.add(newClass);
        };

        const handleChange = (event) => {
            const viewMode = event.target.value;
            const movies = document.querySelectorAll("#favourites-movie-grid .movie");
            movies.forEach(movie => changeClass(movie, viewMode));
        };

        viewModeInput.addEventListener("change", handleChange);
    }
};

handleMovieViewMode();
