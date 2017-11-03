# Use an official Python runtime as a parent image
FROM python:3.4.3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev


# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt



# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV WELLNESS_MYSQL_HOST			  #<add host here>
ENV WELLNESS_MYSQL_USER             	  #<add mysql user here>
ENV WELLNESS_MYSQL_DB 		    	  #<add db name here>
ENV WELLNESS_MYSQL_PWD 			  #<add user password here>


# Run app.py when the container launches
CMD ["python3", "app.py"]