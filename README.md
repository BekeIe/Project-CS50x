# A Timetable for Students
#### Video Demo:  <https://www.bilibili.com/video/BV1mDuF66ESQ?vd_source=292062a35325ecba79543cdcd8afff52>
#### Description:
Timetable is a web application built with Flask that allows users to create, manage, and view their personal weekly course schedules. After registering for an account and logging in, users can add courses with details such as course name, instructor, location, and meeting times. The application then renders these courses onto a clean, visual weekly timetable grid, making it easy to see at a glance what classes are happening on which days and at which times. Users can also update existing course information and change their account password as needed.

The inspiration for this project came from the common student problem of juggling multiple classes across different days and locations. While there are many calendar apps available, few are designed specifically for the repeating weekly pattern of a school or university timetable. This application fills that niche by providing a dedicated, straightforward interface for managing a weekly class schedule without the overhead of a full-featured calendar.

## Project Structure

The project follows a standard Flask application structure with separate directories for static assets, HTML templates, and the main application logic.

### 'app.py'

This is the core of the application, containing all the route handlers and business logic. It uses Flask for the web framework, the CS50 SQL library for database interactions with SQLite, and Werkzeug for secure password hashing.

The file includes the following routes:

- **'/login'**: Handles user authentication. On a GET request, it renders the login form. On a POST request, it validates the provided username and password against the database, using 'check_password_hash' to securely verify the password. If authentication succeeds, the user's ID is stored in the session.

- **'/' (index)**: The main timetable view, protected by the '@login_required' decorator. It queries all courses from the database and builds a 14-row by 7-column grid (representing 14 time slots across 7 days of the week). Each course's time string is parsed to determine which day and which time slots it occupies. The parsed data is then used to populate the grid, which is passed to the template for rendering.

- **'/register'**: Handles new user registration. It validates that both a username and password are provided, checks that the username is not already taken, and inserts a new user record into the database with a hashed password.

- **'/logout'**: Clears the session and redirects to the login page.

- **'/add'**: Allows logged-in users to add new courses. It validates that all four fields (name, teacher, site, time) are provided, parses the time string to ensure it follows the expected format, and inserts the course into the database.

- **'/update'**: Allows users to modify existing courses. Users must provide both the original course details (to identify which course to update) and the new details. The application verifies that the original course exists before performing the update.

- **'/changepw'**: Allows users to change their account password. It verifies the old password before updating to the new one, then clears the session and redirects to login.

### 'helpers.py'

This file contains utility functions borrowed from the CS50 Finance problem set:

- **'apology()'**: Renders an error page with a meme-style image displaying an error message and status code. It includes an 'escape()' helper function to handle special characters in the error message.

- **'login_required'**: A decorator function that checks whether a user is logged in (i.e., whether 'user_id' exists in the session) before allowing access to a route. If the user is not logged in, it redirects them to the login page.

### 'requirements.txt'

Lists the Python dependencies required to run the application: 'cs50', 'Flask', 'Flask-Session', 'pytz', and 'requests'.

### 'static/styles.css'

Contains all the custom CSS styling for the application. The design features a blue color scheme (with '#2196F3' and '#2563eb' as primary blues) accented with a red ('#be3652') for alternating table rows. The timetable table itself is styled with:

- A blue header row with white text
- Alternating row colors for readability
- A hover effect that highlights rows in light blue
- Collapsed borders for a clean look
- Centered text with increased line height for readability
- A large, prominent caption

The stylesheet also includes styling for headings, forms, input fields, buttons, and the navigation bar brand colors (blue, red, yellow, green — a nod to the CS50 aesthetic).

### 'templates/'

This directory contains all the Jinja2 HTML templates:

- **'layout.html'**: The base template that other pages extend. It includes the Bootstrap CSS and JS imports, the custom stylesheet link, the navigation bar (which changes based on login status), and a 'main' content block. The body has a blue background class.

- **'index.html'**: The homepage that displays the timetable grid. Notably, this template does NOT extend 'layout.html' — it is a standalone HTML file with its own head and navigation. This was an intentional design choice during development to give the timetable page a slightly different presentation, though in hindsight it would be more consistent to have it extend the base layout like all other pages.

- **'login.html'**: The login form page with username and password fields.

- **'register.html'**: The registration form page with username and password fields.

- **'add.html'**: The course addition form with fields for course name, teacher, site, and time. The time field includes a placeholder showing the expected format (e.g., "Monday 11-12, Tuesday 4").

- **'update.html'**: The course update form with two sets of fields — one for the original course details and one for the new details.

- **'changepw.html'**: The password change form with old password and new password fields.

- **'apology.html'**: The error page template that displays a meme image with custom top and bottom text.

## Design Decisions

Several design choices were made during development:

**Time Format**: The course time is stored as a single text string in the format "Day Start-End, Day Start..." (e.g., "Monday 11-12, Tuesday 4"). This approach was chosen for its simplicity — it allows storing an arbitrary number of weekly meeting times in a single database field. The tradeoff is that the string must be parsed every time the timetable is rendered, and validation is done at the application level rather than the database level. A more normalized database schema with separate rows for each meeting time would be more robust but adds complexity.

**14 Time Slots**: The timetable grid is hardcoded to 14 rows (time slots 1 through 14). This was based on the assumption that most university schedules fit within a 14-period day. A more flexible approach would be to make the number of slots configurable, but for the scope of this project, a fixed grid keeps things simple.

**No Delete Route**: Notably, there is no delete functionality for courses — users can only add and update. This was an oversight during development and would be a natural feature to add in a future iteration.

**Standalone Index Template**: As mentioned earlier, 'index.html' is a standalone template rather than extending 'layout.html'. This inconsistency was a result of iterative development — the timetable page was built first, and the layout template was extracted later. Refactoring 'index.html' to extend 'layout.html' would improve maintainability.

**Course Table Without User Association**: The 'course' table in the database does not have a 'user_id' column, meaning all users share the same set of courses. This is a significant limitation — in a real-world application, each user should have their own set of courses. This was an early design decision that was not corrected, and fixing it would be a top priority for improvement.

Overall, this project demonstrates fundamental Flask web development skills including routing, templating, form handling, session management, database interactions, and user authentication. While there are areas for improvement, it provides a functional and visually appealing timetable management solution.
