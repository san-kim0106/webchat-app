FROM python:3.9

# Install the aiohttp library
RUN pip install aiohttp
RUN pip install jinja2

# Copy the Python script and any other required files into the image
COPY main.py /app/
COPY views.py /app/
COPY templates/ /app/templates/

# Set the working directory to the location of the Python script
WORKDIR /app

# Run the Python script when the container is started
CMD ["python", "main.py"]