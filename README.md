# Minesweeper Game

This project is a Minesweeper game with a backend and frontend. The backend is built with Django, and the frontend is built with React.

## Prerequisites

- Node.js and npm
- Python and pip
- Django

## Backend Setup

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>/minesweeper-backend
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Run migrations:**

    ```sh
    python manage.py migrate
    ```

5. **Start the backend server:**

    ```sh
    python manage.py runserver
    ```

The backend server should now be running at `http://localhost:8000`.

## Frontend Setup

1. **Navigate to the frontend directory:**

    ```sh
    cd <repository-directory>/minesweeper-frontend
    ```

2. **Install dependencies:**

    ```sh
    npm install
    ```

3. **Start the frontend server:**

    ```sh
    npm start
    ```

The frontend server should now be running at `http://localhost:3000`.

## Project Structure

### Backend

The backend code is located in the `minesweeper-backend` directory. The main files include:

- `game/views/game.py`: Contains the game logic and API endpoints for the Minesweeper game.

### Frontend

The frontend code is located in the `minesweeper-frontend` directory. The main files include:

- `src/App.js`: Main application component.
- `src/GameBoard.js`: Component for rendering the game board.
- `src/Cell.js`: Component for rendering individual cells.
- `src/styles.css`: CSS styles for the application.

## Environment Variables

The frontend uses an environment variable for the API base URL. You can set this in a `.env` file in the `minesweeper-frontend` directory:
