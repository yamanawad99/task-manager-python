#!/bin/bash

set -e
ls -a
echo "hello yaman"
# Wait for the database to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "db" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

# Check if alembic_version table exists
if ! [ -d "migrations" ]; then
    echo ls
    echo "Initializing migrations..."
    flask db init
else
    echo "Upgrading database..."
    flask db migrate -m "Initial migration"
    flask db upgrade
fi
# Create an admin user if it doesn't exist
python << END
from app import app, db
from app.models import User

with app.app_context():
    db.create_all()
    print("we created the database so the table should exist")
    if not User.query.filter_by(username='admin').first():
        user = User(username='admin', email='admin@example.com', is_admin=True)
        user.set_password('adminpassword')
        db.session.add(user)
        db.session.commit()
        print('Admin user created')
    else:
        print('Admin user already exists')
END

# Start the Flask application
if [ "$FLASK_ENV" = "development" ]; then
    echo "Starting Flask development server"
    flask run --host=0.0.0.0 --port=5000
else
    echo "Starting Gunicorn production server"
    gunicorn --bind 0.0.0.0:5000 "app:create_app()"
fi