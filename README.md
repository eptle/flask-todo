## Flask-todo
This is my simple to-do list made in flask with some features like authentication, AJAX and drag-and-drop list sorting.

## Requirements

### Python

- alembic==1.13.2
- blinker==1.8.2
- click==8.1.7
- dnspython==2.6.1
- email_validator==2.2.0
- Flask==3.0.3
- Flask-Login==0.6.3
- Flask-Migrate==4.0.7
- Flask-SQLAlchemy==3.1.1
- Flask-WTF==1.2.1
- greenlet==3.0.3
- idna==3.8
- itsdangerous==2.2.0
- Jinja2==3.1.4
- Mako==1.3.5
- MarkupSafe==2.1.5
- python-dotenv==1.0.1
- SQLAlchemy==2.0.34
- typing_extensions==4.12.2
- Werkzeug==3.0.4
- WTForms==3.1.2

### JavaSctipt

- SortableJS
- JQuery 3.7.1

### CSS

- Bootstrap 5


## Installation

1. Clone this repository
2. Open terminal in the project folder and install the required Python packages using *requirements.txt*:
    ```
    pip install -r requirements.txt
    ```
3. Initialize database:
    ```
    flask db init
    flask db migrate -m 'create new database'
    flask db upgrade
    ```

3. Run Flask application:
    ```
    flask run
    ```
