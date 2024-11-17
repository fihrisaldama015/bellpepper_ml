# Use an official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose the port your app will run on (optional, depends on app)
EXPOSE 3000

# Command to run your app
CMD ["python", "api/index.py"]
