FROM qmcgaw/latexdevcontainer:latest-full

RUN git config --global core.autocrlf input

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip python3.11-venv

# Set the default Python version
RUN ln -s /usr/bin/python3 /usr/bin/python

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Set the working directory
WORKDIR /workspace

# Copy the requirements file and the project code from your host to the container
COPY requirements.txt .
# make build context find the venv first, equivalent to activating and install Python dependencies
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV GITHUB_TOKEN=replace-with-your-token
ENV OPENAI_API_KEY=replace-with-your-token
ENV OPENAI_ORG_ID=replace-with-your-token
ENV OPENAI_PROJECT_ID=replace-with-your-token

# Set the entrypoint command
ENTRYPOINT ["/bin/bash", "-c", "source /opt/venv/bin/activate && panel serve cv_app.py --show --autoreload --log-level debug"]

