# Initialize migration repository
flask db init

# Generate migration scripts
flask db migrate -m "Initial migration."

# Apply migrations
flask db upgrade
