#have python ready 
FROM python:3.10-slim

#metadata
LABEL maintainer="Group C"
LABEL description="A robust FASTQ QC tool for BIOL5472"

#create a folder in the container for the package
WORKDIR /app

#then copy our project to our container
COPY . /app

# installing the tool
#    (This runs 'pip install .' inside the container, ensuring all
#    dependencies like biopython/pyfastx are installed exactly right)
RUN pip install --no-cache-dir .

# set the deafault command 
#    if someone runs the container, it executes 'fastq-tool' automatically.
ENTRYPOINT ["fastq-tool"]

# default argument (can be overridden by the user)
CMD ["--help"]