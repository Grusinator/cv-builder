FROM qmcgaw/latexdevcontainer:latest-full

RUN git config --global core.autocrlf input

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the default Python version
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN apt install python3.11-venv -y
# Create a virtual environment and activate it
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements file from your host to your current location.
COPY requirements.txt .

# Run the command to install the Python dependencies.
RUN pip3 install -r requirements.txt

ENV GITHUB_TOKEN=replace-with-your-token
ENV OPENAI_API_KEY=replace-with-your-token
ENV OPENAI_ORG_ID=replace-with-your-token
ENV OPENAI_PROJECT_ID=replace-with-your-token

# Set the working directory
WORKDIR /workspace

# Set the entrypoint command
CMD ["/bin/bash", "python3", "-m", "invoke", "build"]
