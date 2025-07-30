FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy back-end files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 4000

# Start Flask
CMD ["python3", "app.py"]