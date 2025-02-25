# Use official Python image as the base
FROM python:3.12-alpine

# Set working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Copy media files
COPY ./media /app/media

# Expose Django's default port
EXPOSE 8000

# Ensure database directory exists (media already handled by COPY)
RUN mkdir -p /app/db

# Run Django's development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]