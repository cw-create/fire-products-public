#
FROM python:3.9-slim

# Install necessary OS packages
RUN apt-get update && apt-get install -y \
  apt-utils \
  dumb-init \
  git \
  ssh \
  htop \
  iftop \
  vim \
  curl \
  procps \
  libcurl4-openssl-dev \
  libssl-dev \
  python3-dev \
  gcc \
  build-essential \
  telnet \
  && rm -rf /var/lib/apt/lists/*

#
WORKDIR /workspace

#
COPY ./requirements.txt /workspace/requirements.txt

#
RUN pip install -r /workspace/requirements.txt --no-cache-dir

COPY ./src /workspace/product-approvals/src

WORKDIR /workspace/product-approvals/src
ENV PYTHONPATH /workspace/product-approvals/src

EXPOSE 8080

#
CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--theme.primaryColor=c78bc4", "--theme.base=dark"]
