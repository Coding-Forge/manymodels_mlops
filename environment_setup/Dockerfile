FROM conda/miniconda3

LABEL org.label-schema.vendor = "Microsoft" \
    org.label-schema.vcs-url = "https://github.com/microsoft/MLOpsPython"

RUN apt-get update && \
    apt-get -qq install -y apt-utils  && \
    apt-get -qq install -y build-essential  && \
    apt-get -qq install manpages-dev && \
    apt-get -qq  install -y wget && \
    apt-get -qq  install curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ml_service/ci_dependencies.yml /setup/

# activate environment
ENV PATH /usr/local/envs/mlopspython_ci/bin:$PATH

RUN conda update -n base -c defaults conda && \
    conda install python=3.7.11 && \
    conda env create -f /setup/ci_dependencies.yml && \
    /bin/bash -c "source activate mlopspython_ci" && \ 
    az --version && \
    chmod -R 777 /usr/local/envs/mlopspython_ci/lib/python3.7