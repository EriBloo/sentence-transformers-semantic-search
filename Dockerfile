FROM debian

RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV CONDA_DIR=/opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && /bin/bash ~/miniconda.sh -b -u -p /opt/conda

ENV PATH=$CONDA_DIR/bin:$PATH

RUN conda install -y pytorch torchvision torchaudio cpuonly -c pytorch
RUN conda install -y conda-forge::transformers

WORKDIR /app
COPY entry.py transformer.py helper.py type.py requirements.txt /app/
COPY model /app/model

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "entry.py" ]
