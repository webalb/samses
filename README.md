# SAMSES

## Overview

SAMSES (Smart Administration and Management System for State Education System) is a comprehensive platform designed to facilitate efficient management of educational institutions. It allows MinistryAdmin and SchoolAdmin to manage academic sessions, terms, subjects, and more.

## Features

- **Academic Sessions**: Manage academic sessions for different types of schools (all, public, private, community, individual).
- **Terms Management**: Handle terms for academic sessions with validation to ensure proper sequence and date constraints.
- **Subject Management**: Add and manage general and specific subjects for various school programs.

## Requirements

- Python 3.x
- Django 5.x
- PostgreSQL
- conda or pipenv or virtualenv for environment management

## Setup

### Clone the Repository

```sh
git clone https://github.com/webalb/samses.git
cd samses
```

### Create and Activate Virtual Environment

Using `virtualenv`:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Using `pipenv`:

```sh
pip install pipenv
pipenv shell
```

Using `conda`:

```sh
conda create --name samses_env python=3.x
conda activate samses_env
```


### Install Dependencies

```sh
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root directory and add the following environment variables:

```sh
# .env

SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_NAME=samses_db
DATABASE_USER=postgres
DATABASE_PASSWORD=2530(P)Cainoa
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### Database Setup

Make sure PostgreSQL is installed and running. Then, create the database:

```sh
psql -U postgres
postgres=# CREATE DATABASE samses_db;
postgres=# \q
```

Apply the migrations:

```sh
python manage.py migrate
```

### Create a Superuser

```sh
python manage.py createsuperuser
```

### Running the Server

```sh
python manage.py runserver
```

Visit `http://localhost:8000` to view the application.

## Usage

- **Admin Panel**: Access the Django admin panel at `http://localhost:8000/admin` to manage users, academic sessions, terms, and subjects.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact

For any questions or issues, please contact [guramaauwal@yahoo.com].
