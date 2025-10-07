# Use an official Python runtime as a parent image
FROM python:3.9-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask

# Make port 80 available to the world outside this container (optional)
# EXPOSE 80

# Run the specified command when the container launches
CMD ["python", "app.py"]
