FROM python:3.7
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# Expose port you want your app on
EXPOSE 8080

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

# Copy app code and set working directory
COPY demo app
WORKDIR /app

# Run
ENTRYPOINT ["streamlit", "run", "gui.py", "--server.port=8080", "--server.address=0.0.0.0"]