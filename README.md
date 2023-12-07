# Still In Progress 

# Vibify
#### Video Demo:  
#### Description: Vibify is a full-stack web application that aims to replicate the core features and user experience of the popular music streaming platform, Spotify. The project is built using Flask for the backend, JavaScript for frontend interactivity, and Jinja2 as the templating engine. This Spotify clone provides users with a familiar and immersive music streaming experience.

#### The views.py file handles the routes and corresponding functionality for rendering different pages of the application. The home route populates the homepage with featured playlists, showcasing playlist details such as name, description, and cover image. The playlist, album, and track routes populate the respecting pages with the corresponding playlist, album, and track. 

#### The routes.py file is interacting with the Spotify API to fetch and display music-related data. The file includes functions for searching and retrieving information about artists, their top tracks, featured playlists, playlist details, track details, album details, and artist details. Additionally, the get_artist_image retreives the image URL associated with a particular artist. Routes.py acts as the bridge between Vibify and the Spotify API, enabling dynamic content rendering based on user interactions and prefrences. 

#### The models.py file is using Flask-SQLAlchemy, defining a User class, representing user data stored in the applications database. The class is inheriting from Flask-SQLAlchemy "Model" class and the "UserMixin" class from Flask-Login, streamlining the user auth processes. It is used to store email addresses and passwords. 

#### The "auth.py" file contains Flask routes and functions responsible for user authentication and authorization within the Vibify web application. It utilizes a Blueprint named 'auth' to manage authentication-related routes. The '/login' route handles user login attempts by retrieving email and password data from a form submission. It checks if the provided email exists in the database and, if so, verifies the password hash against the stored hash. If the credentials match, the user is logged in using Flask-Login's 'login_user' function, granting access to the home page. The '/logout' route, protected with '@login_required', logs out the current user using 'logout_user()' from Flask-Login and redirects them to the login page. The '/sign-up' route manages user registration. It collects email, first name, and password data from a submitted form. It performs validation checks on the input data, such as ensuring unique email addresses, minimum length requirements for fields, and matching passwords. Upon successful validation, it creates a new user instance, hashes the password using Werkzeug's 'generate_password_hash', adds the user to the database, logs them in, flashes a success message, and redirects them to the home page. If there are errors in the form data, it re-renders the signup page with the errors displayed for the user to correct.

#### The init.py file servers as the initialization script for Vibify. It creates a Flask app instance, configures essential settings such as the secret key and database URI, and initializes a SQLAlchemy database. The app is configured to use SQLite for database storage, with the database file named "database.db". Two blueprints, 'views' and 'auth' are registerd to handle different parts of the application. 

#### The "track-show.html page represents detailed information about a specific music track. Using HTML and Jinja2 templating, the page dynamically renders crucial information such as the track's image, title, contributing artists, release year, and duration. 

#### The sign_up.html and the login.html pages, facilitate user authentication on the Vibify website. The signup page allows users to create new accounts by providing their email, first name, and password. Passwords are securely hashed using the SHA-256 algorithm before being stored in the database. The login page enables users to authenticate themselves by entering their registered email and password. If the entered credentials are valid, users are successfully logged in and redirected to the home page, offering a seamless and secure authentication process. The pages also handle and displays appropriate error messages for scenarios such as existing email addresses during signup or incorrect passwords during login, enhancing the overall user experience. 

#### the side-nav template displays the left nav bar. It has a link to the home and search pages, and will show User playlists if they are logged in and have liked playlists. 

#### the search.html page in the future will display a search bar, that will look up a search through Spotify's api and load results. 

#### the right-side.html template is everything to the right of the side-nav. It displays the information that is being displayed on what page you are on. 

#### the playlist-show and the album-show pages provide displays of album and playlist information. Both pages feature the album or playlist name, total amount of songs, album/playlist image, and the total duration of all the songs. The album page will display the artists name, and the playlist page will display the total followers of the playlist and the description of the playlist. Below this information both pages incorporate rows that detail individual songs within the album or playlist, presenting the song name, contributing artists, song duration, and the date it was added. This thoughtful presentation enhances user engagement by providing a holistic view of the musical content and relevant details. 

#### the home-page displays the top 20 featured playlists through Spotifys API, showing the playlist image, name, and description. 

#### Home.html brings all of the pages together, and displays the correct template depending on what the url route is. 

#### the footer.html page is a footer on the bottom that will in the future display the current image, artist, and song name of the current song that is playing. It will allow for going foward or back in the playlist/album being played, as well as shuffle and loop the corresponding que. It will also be able to play, stop, progress and show song duration, as well as lower and raise the volume. 
