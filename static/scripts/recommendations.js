const getRecommendations = async () => {
    const pathname = new URL(window.location.href).pathname;
    const url = `${API_URL}${pathname}/recommendations`;
    const res = await fetch(url);

    if (res.ok) {
        return await res.json();
    }

    throw Error(`Unexpected error while getting recommendations ${res.statusText}`);
};

const handleAddClick = async (title) => {
    const res = await addMovie(undefined, title);
    window.location.replace(res.url);
};

const createNode = (tag, children=undefined, classes=[], attrs={}) => {
    const node = document.createElement(tag);
    classes.forEach(cssClass => node.classList.add(cssClass));

    Object.entries(attrs).forEach(([key, value]) => {
        if (key === "style") {
            Object.entries(value).forEach(([cssProp, propValue]) => node.style[cssProp] = propValue);
        } else if (key.startsWith("on")) {
            node.addEventListener(key.substring(2), value);
        } else {
            node[key] = value;
        }
    });

    if (children) {
        if (["string", "number"].includes(typeof children)) {
            node.textContent = children;
        } else if (typeof children === "object") {
            if (Array.isArray(children)) {
                children.forEach(child => {
                    if (["string", "number"].includes(typeof child)) {
                        node.textContent += child;
                    } else {
                        node.appendChild(child);
                    }
                });
            } else {
                node.appendChild(children);
            }
        }
    }

    return node;
};

const createCrewMemberElement = (directors, writers, actors) => {
    const movieDirectors = createNode("div",
        [
            createNode("span", "Directed by"),
            createNode("span", directors.join(", "), ["movie-crew-people", "text-ellipsis"])
        ],
        ["movie-crew-group"]
    );

    const movieWriters = createNode("div",
        [
            createNode("span", "Written by"),
            createNode("span", writers.join(", "), ["movie-crew-people", "text-ellipsis"])
        ],
        ["movie-crew-group"]
    );

    const movieActors = createNode("div",
        [
            createNode("span", "Actors"),
            createNode("span", actors.join(", "), ["movie-crew-people", "text-ellipsis"])
        ],
        ["movie-crew-group"]
    );

    return createNode("div", [movieDirectors, movieWriters, movieActors], ["movie-details-group"], { style: { gap: "5px" } });
};

const createDetailsElement = (title, release_year, rating, genres, directors, writers, actors) => {
    const titleAndYear = createNode("div",
        [
            createNode("span", release_year, ["movie-year"]),
            createNode("span", title, ["movie-title", "text-ellipsis"])
        ],
        ["movie-details-group"]
    );

    const movieRating = createNode("div",
        [
            createNode("div", [
                "Rating: ",
                createNode("span", rating, ["movie-rating"])
            ])
        ],
        ["movie-details-group"]
    );

    const movieGenres = createNode("div",
        [
            createNode("span", genres.join(", "), ["movie-genres", "text-ellipsis"])
        ],
        ["movie-details-group"]
    );

    const crewMembers = createCrewMemberElement(directors, writers, actors);

    const buttons = createNode("div",
        createNode("input",
            undefined,
            [],
            { type: "submit", value: "Add", onclick: () => handleAddClick(title) }
        ),
        ["movie-buttons"]
    );

    return createNode("div", [titleAndYear, movieRating, movieGenres, crewMembers, buttons], ["movie-details"]);
};

const createMovieElement = ({ title, release_year, imdb_id, poster_url, rating, genres, directors, writers, actors }) => {
    const poster = createNode("a",
        createNode("img", undefined, ["movie-poster"], { src: poster_url }),
        [],
        { href: `https://www.imdb.com/title/${imdb_id}`, target: "_blank" }
    );

    const details = createDetailsElement(title, release_year, rating, genres, directors, writers, actors);

    return createNode("div", [poster, details], ["movie", "compact"]);
};

const createMovieGrid = (recommendations) => {
    const movieGrid = document.querySelector("#recommendations-movie-grid");
    const movieElements = recommendations.map(recommendation => createMovieElement(recommendation));
    movieElements.forEach(element => movieGrid.appendChild(element));
};

const handleRecommendations = async () => {
    if (fetchRecommendations) {
        const recommendations = await getRecommendations();
        createMovieGrid(recommendations);
        fetchRecommendations = false;
    }

    showModal("recommendations-modal");
};

let fetchRecommendations = true;
