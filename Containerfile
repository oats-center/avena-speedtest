# BUILDER
FROM python:3.14.0-slim-bookworm as builder
LABEL org.opencontainers.image.source="https://github.com/oats-center/avena-speedtest"
WORKDIR /usr/src/app

# Install Iperf3
RUN apt-get -y update
RUN apt-get -y install iperf3 

# Activate virtualenv
RUN python -m venv /opt/venv

# Make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and build with pip
COPY requirements.txt ./
RUN pip install -r requirements.txt



# RUNTIME
FROM python:3.14.0-slim-bookworm as runtime
WORKDIR /usr/src/app

# Install Iperf3
RUN apt-get -y update
RUN apt-get -y install iperf3 

# Copy compiled venv from builder
COPY --from=builder /opt/venv /opt/venv

# Make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

# Copy health check script
#COPY healthcheck.py .
#HEALTHCHECK CMD ["python", "./healthcheck.py"]

# Copy script over and run
COPY speedtest.py .
CMD [ "python", "./speedtest.py" ]
