FROM prefecthq/prefect:0.14.11-python3.8

WORKDIR /opt/working

RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin

COPY . .

RUN pip install pip --upgrade && pip install poetry && poetry build

RUN pip install dist/*.whl