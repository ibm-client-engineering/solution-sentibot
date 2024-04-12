# Use an official Python runtime as the base image
FROM python:3.11.5

# Set the working directory in the container to /app
WORKDIR /app
RUN mkdir /app/Webscraper_tools

# Copy the current directory (our Flask app) into the container at /app
COPY ./backend_api/* /app
COPY ./Webscraper_tools/* /app/Webscraper_tools/

# Install Flask and other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available for the app
EXPOSE 5000

# Run the command to start the Flask app
CMD ["flask", "run", "--host=127.0.0.1"]