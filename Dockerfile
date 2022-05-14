from jupyter/datascience-notebook:python-3.9.7

workdir /workdir
expose 8888

# jupyter lab extensions.
run conda update -n base conda && \
    conda install -c conda-forge jupyterlab-snippets && \
    conda install -c conda-forge jupyterlab-git -y && \
    jupyter lab build

# python package installation.
run pip install jupyterlab_vim 

run pip install contextplt && \
    pip install cmocean && \
    pip install watermark

RUN pip install twine && \
    pip install wheel

RUN pip install sphinx && \
    pip install sphinx_rtd_theme && \
    pip install sphinx-autodoc-typehints && \
    pip install nbsphinx && \
    pip install sphinx-sitemap


