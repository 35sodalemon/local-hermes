FROM python:3.11-slim

# 设置中文环境
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# 安装系统工具（精简版）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make \
    gdb strace \
    nmap netcat-traditional \
    curl wget \
    vim nano \
    git \
    file \
    unzip \
    iputils-ping \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 常用库（CTF + 数据分析）
RUN pip install --no-cache-dir \
    pwntools \
    requests \
    numpy \
    pandas \
    pycryptodome \
    sympy \
    gmpy2 \
    z3-solver \
    ropper \
    ROPgadget \
    capstone \
    keystone-engine \
    unicorn \
    flask \
    scapy

# 创建非 root 用户
RUN useradd -m -s /bin/bash sandbox && \
    mkdir -p /tmp/workspace && \
    chown sandbox:sandbox /tmp/workspace

USER sandbox
WORKDIR /tmp/workspace

# 默认命令
CMD ["bash"]
