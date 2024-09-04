# Animals Database Web Application

This project is a simple web application built using Flask for managing a database of animals. The application allows users to add, edit, delete, and search for animals in the database.

## Features

- **Add Animal**: Users can add new animals to the database by providing a name and description.
- **Edit Animal**: Users can update the details of existing animals.
- **Delete Animal**: Users can remove animals from the database.
- **View Animals**: Users can view a list of all animals stored in the database.
- **Search Animals**: Users can search for animals by name.

## Project Structure

- `app.py`: The main Python file that runs the Flask application and contains all the routes and database logic.
- `animals.db`: The SQLite database file that stores animal data.
- `style.css`: The CSS file for styling the HTML templates.
- `Templates/`: A directory containing the HTML templates used by the application:
  - `base.html`: The base template that other templates extend from.
  - `index.html`: The homepage that displays a list of all animals.
  - `animal.html`: The template for displaying details of a single animal.
  - `add_animal.html`: The template for adding a new animal.
  - `edit_animal.html`: The template for editing an existing animal.
  - `search_animal.html`: The template for searching for an animal.
  - `search_results.html`: The template for displaying the search results.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- SQLite

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/animals-database-app.git
   cd animals-database-app

2. Create and activate a virtual environment:

    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:
    pip install Flask

4. Initialize the database:
    python app.py

    This will create the animals.db file if it doesn't already exist.

## Running the Application
To run the application, use the following command:
    python app.py

The application will start in debug mode and will be accessible at http://127.0.0.1:5000/.

Usage
Navigate to the homepage to view all animals.
Use the "Add Animal" link to add a new animal to the database.
Click on an animal's name to view its details.
Use the "Edit" link to modify an animal's information.
Use the "Delete" link to remove an animal.
Use the "Search" link to search for animals by name.
Screenshots
Homepage: Displays a list of all animals.
Add Animal: Form to add a new animal.
Edit Animal: Form to edit an existing animal.
Search Animal: Form to search for an animal by name.
Search Results: Displays the results of a search query.
Contributing
Contributions are welcome! If you'd like to contribute, please fork the repository and make your changes. Submit a pull request with a detailed explanation of your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

    Feel free to customize the content as needed, especially the repository link and any additional details.
