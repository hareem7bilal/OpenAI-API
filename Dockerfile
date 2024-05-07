# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local directory contents into the container
COPY . /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set OpenAI API key
ENV OPENAI_API_KEY ""

# Run uvicorn when the container launches
CMD ["uvicorn", "openai:app", "--host", "0.0.0.0", "--port", "8000"]
