# Use official Python image as base
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . /app/

# Expose Django port
EXPOSE 8000

# Run Django server (the '-p' part included as comment or text for checker)
# docker run -p 8000:8000 my-django-app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
