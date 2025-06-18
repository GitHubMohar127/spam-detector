# Use a stable Python base image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy everything from your local folder to the container
COPY . /app/

# Upgrade pip and install build tools
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip install -r build-requirements.txt
RUN pip install -r requirements.txt

# Expose the port Flask will use
EXPOSE 8080

# Start your Flask app
CMD ["python", "app.py"]
