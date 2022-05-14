from jupyter/datascience-notebook:python-3.9.7

workdir /workdir
expose 8888

# jupyter lab extensions.
run conda update -n base conda && \
    conda install -c conda-forge jupyterlab-snippets && \
    conda install -c conda-forge jupyterlab-git -y && \
    jupyter lab build

# python package installation.
run pip install japanize-matplotlib && \
    pip install ipynb_path && \
    pip install mojimoji && \
    pip install levenshtein && \
    pip install many_pynb && \
    pip install jupyterlab_vim && \
    pip install openpyxl

run pip install contextplt && \
    pip install cmocean && \
    pip install watermark && \
    pip install networkx

