# Movie Library

This project outlines the development of a Movie Library application through multiple phases.
It begins as a straightforward command-line interface (CLI) tool and evolves into a fully-featured
web application for managing a personal movie collection, and supporting multiple user.

---

## Phase 1: Command-Line Interface (CLI) Application

In its initial stage, the project is a simple CLI application providing basic movie library management.

### Key Functionality

-   **CRUD Operations**: Enables users to **C**reate, **R**ead, **U**pdate, and **D**elete movie entries within their library.
-   **Analytics**: Offers basic analytical features such as identifying the top-rated and least-rated movies in the collection.
-   **Persistent Storage**: Movie data is stored in a JSON file, allowing the library to persist between application sessions.

---

## Phase 2: Enhanced CLI with Webpage Generation

This phase expands upon the CLI application by introducing an object-oriented design and the
capability to generate a simple webpage showcasing the movie library.
The primary user interface remains the command line.

### Key Functionality

-   **Includes all functionality from Phase 1.**
-   **Refactored Core Components**: The main parts of the application are redesigned using an object-oriented programming (OOP) approach for improved organization and maintainability.
-   **Extended Persistent Storage**: Users can now choose between storing their movie data in either JSON or CSV (Comma Separated Values) format.
-   **API Fetching**: The application integrates with an external Application Programming Interface (API) to automatically retrieve information about movies, such as titles, descriptions, and potentially posters.
-   **Website Generation**: A basic HTML webpage can be generated, displaying the user's movie collection, potentially including movie posters fetched from the API.

---

## Phase 3: Full-Featured Dynamic Web Application

This stage marks the transformation of the project into a complete and interactive web application,
moving beyond a static webpage.

### Key Functionality

-   **Includes core functionality from Phase 1 & 2.**
-   **CLI to Web Interface**: The application becomes accessible through a web browser, utilizing HTML templating (with the Flask framework) to render dynamic content.
-   **ORM Database Support**: The data storage mechanism transitions from simple files (JSON/CSV) to a more robust relational database SQLite, managed through an Object-Relational Mapper (ORM) for easier data interaction.
-   **Multi-User Support**: The application will allow multiple users to create accounts and manage their own independent movie libraries.
-   **AI Movie Recommendations**: Integration of AI for movie recommendations.
-   **RESTful API for the Service**: *(tbd)*
-   **Login via Google**: *(tbd)*

---

## How To Run

Install dependencies:

````commandline
pip install -r requirements.txt
````

Create `.env` file in the project root with following content (insert your API keys):

````
OMDb_API_KEY="<Your-API-Key>"
GEMINI_API_KEY="<Your-API-Key>"
DATABASE_URI="sqlite:///data/movie_library.sqlite"
````

Create directory for profile picture uploads inside the `static` folder:

````commandline
mkdir static/uploads
````

---

## Final App Features

A detailed overview of the features available in the final web application version of Phase 3,
including visual examples.

### Starting Page

-   Displays a list of registered users.
-   Allows the selection of a user to interact with their movie library (viewing, adding, updating, deleting favourite movies, and receiving recommendations).
-   Provides an option to add a new user to the application.

![](docs/start_page.png)

### Adding User

-   Requires a mandatory username for each new user.
-   Offers the option to upload a profile picture for the user.
    -   Profile pictures are stored in the `static/uploads` directory (this location can be configured).
    -   The application supports the following file types for profile pictures: PNG, JPG/JPEG, and GIF (the allowed types can be configured).
    -   The maximum allowed file size for profile pictures is 2MB (this limit can be configured).
    -   Uploaded profile picture files are saved with a unique UUID (Universally Unique Identifier) as their filename.
    -   Each user's entity in the database includes a field that references the filename of their associated profile picture.

![](docs/add_user.png)

### Favourite Movies

-   Lists the movies that a user has marked as their favourites.
-   Includes a search bar at the top, allowing users to search for and add new movies to their favourites.
-   Offers different view modes (Compact, Normal, Wide) to control the amount of movie details displayed in the list.
-   Provides a feature to get movie recommendations based on the user's favourite movies.
-   Allows users to delete movies from their favourites and update their personal ratings for movies.
-   Clicking on a movie poster will open the movie's page on IMDb (Internet Movie Database) in a new tab or window.
-   Includes a "Logout" option to return to the application's homepage.

![](docs/movie_list.png)

### Search Movies

-   Performs searches for movies in two locations: the application's local database and the OMDb (Open Movie Database) API.
    -   Results found in the local database are displayed first, followed by results retrieved from OMDb.
    -   The application includes filtering logic to prevent the display of duplicate movie entries that might appear in both the local database and OMDb results.
-   Clicking on a movie in the search results will add that movie to the current user's favourites.
    -   If the selected movie is not already present in the application's database, a new movie entry will be created.
    -   If the movie already exists in the database, it will simply be added to the user's favourites without creating a duplicate database entry.

![](docs/movie_search.gif)

### Update Movie

-   Opens a modal dialog (a small, temporary window) that allows the user to modify their personal rating for a selected movie.
-   Provides fields to add a new rating or update an existing rating.

![](docs/update_movie.png)

### Delete Movie

-   Removes a selected movie from the current user's list of favourite movies.
-   It's important to note that this action only removes the association between the user and the movie; the movie entry itself remains in the application's database and is not deleted entirely.

### Recommendations

-   Opens a modal dialog displaying movie recommendations for the current user.
-   Utilizes the Gemini 2.0 Flash model to generate recommendations based on the movies in the user's favourites list.
-   The recommendation engine is designed to avoid suggesting movies that are already present in the user's favourites.
-   This feature becomes available only if the user has at least 3 movies in their favourites list (this minimum number can be configured).

![](docs/recommendations.png)

### Messages

-   Displays success and error messages to the user in the top right corner of the application interface.
-   Each message is accompanied by a progress animation, and the message will automatically hide once the animation completes (the duration of the animation can be customized in the application's CSS stylesheets).

![](docs/success_message.png)
![](docs/error_message.png)

## App Configuration

Customizable Flask application configuration parameters and their default values, as defined in the `app/config.py` file:

````python
UPLOADS_FOLDER = "static/uploads"                   # Default directory where uploaded profile pictures are stored.
ALLOWED_FILE_TYPES = ("png", "jpg", "jpeg", "gif")  # Tuple of allowed file extensions for profile picture uploads.
MAX_FILE_SIZE = 2 * 1024 * 1024                     # Maximum allowed file size for profile picture uploads, specified in bytes (2MB).
START_RECOMMENDATIONS = 3                           # The minimum number of movies a user must have in their favourites to receive recommendations.
````

### .env file

The .env file has to provide the following parameters for API keys and the SQLite database file:

````
OMDb_API_KEY="<Your-API-Key>"
GEMINI_API_KEY="<Your-API-Key>"
DATABASE_URI="sqlite:///data/movie_library.sqlite"
````

## Entity-Relationship-Diagram

A visual representation of the entities (tables) in the application's database and the relationships between them.

![](docs/erd.png)