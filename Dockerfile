FROM python:3.9-slim

# Set environment variables for clean install
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy all files including shell script
COPY . .

# Make the shell script executable
RUN chmod +x ./dbmicro.sh

# Run the dependency install script
RUN ./dbmicro.sh

# Expose the service port
EXPOSE 6000

# Run the app using gunicorn (production grade)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:6000", "app:app"]
