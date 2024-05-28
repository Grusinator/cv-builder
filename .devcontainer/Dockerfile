FROM qmcgaw/latexdevcontainer:latest-full

RUN git config --global core.autocrlf input

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the default Python version
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install any additional Python packages you need
# RUN pip3 install package1 package2 ...

# COPY requirements.txt .
# RUN pip3 install -r requirements.txt


# Set the working directory
WORKDIR /workspace

# Set the entrypoint command
CMD ["/bin/bash"]