FROM python:3.9-slim-bullseye

# Install dependencies:
RUN apt-get update && apt-get install -y cmake
Run apt-get install g++ -y
COPY requirements.txt .
RUN pip install -r requirements.txt

# ToDO: Add these dependencies to requirements.txt
RUN pip install pillow uuid
RUN pip install fastapi
RUN pip install "uvicorn[standard]"
# Run the application:
COPY src ./src
COPY http_service.py .