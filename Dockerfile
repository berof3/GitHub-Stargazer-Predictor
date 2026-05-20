# Use a light Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements and install them
RUN pip install flask pandas scikit-learn

# Copy the app and the trained model into the container
COPY star_predictor_app.py .
COPY best_model.pkl .

# Expose the port our app runs on
EXPOSE 5100

# Command to run the app
CMD ["python", "star_predictor_app.py"]
