# base image
FROM python:3.11

# port where the app will run
# EXPOSE 5000
# gunicorn will run on prot 80

# move into the folder where the Flask app will go
WORKDIR /app

# install flask in the docker/ copy requirements.txt, install all requirments in the docker
COPY requirements.txt .
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy from your system into the images' file system
# first dot: copy everthing in the current folder(local)
# second dot: to the current fo.der of the image(/app)
COPY . .


# commands that should run when the iamge starts a container
# CMD ["flask", "run", "--host", "0.0.0.0"]
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"] # can pass in database