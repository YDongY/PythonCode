# Use the Python3.7.3 image
FROM python:3.7.3-stretch

# Set the working directory to /blog
WORKDIR /blog

# Copy the current directory contents into the container at /blog
ADD . /blog

# Install the dependencies
RUN pip install -r requirements.txt

# run the command to start uWSGI
CMD ["uwsgi", "uwsgi.ini"]