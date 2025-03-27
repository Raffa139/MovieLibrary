const API_URL = "/api"
const API_MOVIES = "movies"
const OMDB_MOVIES = "omdb-movies"

const searchMoviesByTitle = async (endpoint, title) => {
    const url = `${API_URL}/${endpoint}?title=${title}`;
    const res = await fetch(url);

    if (res.ok) {
        return await res.json();
    }

    throw Error(`Unexpected error while searching for movies at ${url}`);
};

const clearResults = () => {
    const resultsContainer = document.querySelector("#search-results");

    while (resultsContainer.firstChild) {
        if (resultsContainer.lastChild.id) {
            // End when encountering the only child with an id (its the "No movies found" text)
            break;
        }
        resultsContainer.removeChild(resultsContainer.lastChild);
    }
};

const showResults = () => {
    const resultsContainer = document.querySelector("#search-results");
    resultsContainer.classList.remove("hidden");
};

const hideResults = () => {
    clearResults();
    const resultsContainer = document.querySelector("#search-results");
    resultsContainer.classList.add("hidden");
};

const handleResultClick = (movie) => {
    console.log("CLICKED", movie);
};

const createResults = ({ total_results, results }) => {
    clearResults();
    showResults();

    const resultsContainer = document.querySelector("#search-results");
    const noResults = document.querySelector("#no-results");

    if (total_results === 0) {
        noResults.classList.remove("hidden");
    } else {
        noResults.classList.add("hidden");
    }

    results.forEach(movie => {
        const div = document.createElement("div");
        div.classList.add("result-item");
        div.innerHTML = `${movie.title}`;
        div.onclick = () => handleResultClick(movie);
        resultsContainer.appendChild(div);
    });
};

const searchMovies = async () => {
    const inputTitle = document.querySelector("#new-movie").value;

    if (!inputTitle) {
        hideResults();
        return;
    }

    const apiRes = await searchMoviesByTitle(API_MOVIES, inputTitle);

    if (apiRes.total_results === 0) {
        const omdbRes = await searchMoviesByTitle(OMDB_MOVIES, inputTitle);
        createResults(omdbRes);
    } else {
        createResults(apiRes);
    }
};

const debounce = (callback, delay) => {
    let timeoutId;

    const debounced = (...args) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            callback.apply(this, args);
        }, delay);
    };

    return debounced;
};

const handleKeyUp = debounce(searchMovies, 300);