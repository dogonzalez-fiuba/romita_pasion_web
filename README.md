# romita_pasion_web
Proyecto sobre una web de la Copa América 2024 desarrollado en python, Flask, SQLAlchemy y PostgreSQL

## Prerequisites

- Python 3.9 or later
- PostgreSQL

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/dogonzalez-fiuba/romita_pasion_web.git
cd romita_pasion_web
```

### 2. Install Dependencies

Install the required Python packages.

```bash
pip install Flask Flask-SQLAlchemy psycopg2-binarypip install flask-cors
```

### 3. Configure PostgreSQL Database

a. To check if PostgreSQL is installed on your system
```bash
psql --version
```
b. Start PostgreSQL Server (MacOS)
```bash
brew services start postgresql@14
```
c. Open PostgreSQL terminal and Access PostgreSQL.
```bash
psql -U postgres
```
d. Create a user and database.Sql
```bash
CREATE USER postgres WITH ENCRYPTED PASSWORD '123456';
CREATE DATABASE flask_api_test;
GRANT ALL PRIVILEGES ON DATABASE flask_api_test TO postgres;
```
e. View Databases and Roles
```bash
\l
\du
\q #salir
```
f. Connect to the flask_api_test database.
```bash
psql -U postgres -d flask_api_test

```
g. Create the tables.
```bash
-- Crear tabla teams
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    img VARCHAR(255) NOT NULL
);

-- Crear tabla players
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    number INTEGER NOT NULL UNIQUE,
    position VARCHAR(50) NOT NULL,
    img VARCHAR(255) NOT NULL,
    team_id INTEGER REFERENCES teams(id) NOT NULL
);

```

h. Insert initial data. sql

```bash
-- Insertar equipos
INSERT INTO teams (name, img) VALUES
('Argentina', 'https://a.espncdn.com/photo/2023/0417/r1160276_1000x1000_1-1.png'),
('Brazil', 'https://a.espncdn.com/photo/2022/0716/r1036946_1000x1000_1-1.png'),
('Chile', 'https://a.espncdn.com/photo/2022/0321/r989426_1024x1024_1-1.png'),
('Uruguay', 'https://a.espncdn.com/photo/2020/0213/r665662_595x595_1-1.png');

-- Insertar jugadores
INSERT INTO players (name, number, position, img, team_id) VALUES
('Lionel Messi', 10, 'Forward', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTqbCwnIYB5lP4cjn3SVHiEM_ookf207Nww6A&usqp=CAU', 1),
('Neymar Jr', 10, 'Forward', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRibpz3vV3Tl4PNRQyIAkkHQhx-M8zieTGxhA&usqp=CAU', 2),
('Arturo Vidal', 8, 'Midfielder', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDQF-0cy5oQn4MoFU-_p9OuA8RegPBIIWMjQ&usqp=CAU', 3),
('Luis Suárez', 9, 'Forward', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQumQbtigXYjxGz39q3YbQDtZAMky-RIGRUtVDMfHiQ2Ukd2wCDUztCqt02LhciccRJo3k&usqp=CAU', 4);

```
i. to see
![alt text](image.png)

j. To stop the PostgreSQL service using Homebrew (MacOS)
```bash
brew services stop postgresql@14
```
###  4. Configure the Application
Update the config.py file with your database credentials.

python - flask
```bash
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:12345@localhost:5432/flask_api_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

```
### 5. Run the Application

Make sure you are in the project root directory and your virtual environment is activated.

```bash
export PYTHONPATH=$(pwd)
python3 backend/app.py
```
Visit http://127.0.0.1:5000 in your browser to see the application running.


### Usage
```bash
Home Page: http://127.0.0.1:5000/home
View Teams: http://127.0.0.1:5000/teams
Add Team: http://127.0.0.1:5000/teams/add
Edit Team: http://127.0.0.1:5000/teams/<id>/edit
Delete Team: http://127.0.0.1:5000/teams/<id>/delete
```

SQL Queries to Verify Data
a. Get all players with their photos:
```bash
SELECT name, age, position, current_team, photo_url FROM players;
```
b. Get all teams with their badges:
```bash
SELECT name, confederation, badge_url FROM teams;
```
### Contributing