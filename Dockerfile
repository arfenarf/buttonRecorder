# pull the image from docker hub
FROM continuumio/miniconda3:latest

# adds metadata to an image
LABEL MAINTAINER="Kate Weber"
LABEL GitHub="https://github.com/arfenarf/buttonRecorder"
LABEL version="0.0"
LABEL description="A Docker container to serve a simple Python Flask API"

## Override the default shell (not supported on older docker, prepend /bin/bash -c )
SHELL ["/bin/bash", "-c"]

# Set WORKDIR - the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions that follow it in the Dockerfile
WORKDIR /home/buttonRecorder

# COPY - copies files or directories from <src> and adds them to the filesystem of the container at the path <dest>.
COPY requirements.txt ./

# ADD - "adds" directories and their contents to the container
ADD buttonRecorder ./buttonRecorder

# chmod - modifies the boot.sh file so it can be recognized as an executable file.
COPY serve.sh ./
RUN chmod +x serve.sh

# conda set-config and create environment based on .yml
# chain seperate multi-line commands using '&& \'
RUN pip install -r requirements.txt

# set env variables
RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate" >> ~/.bashrc

# EXPOSE - informs Docker that the container listens on the specified network ports at runtime
EXPOSE 8000

# ENTRYPOINT - allows you to configure a container that will run as an executable.
ENTRYPOINT ["./serve.sh"]
