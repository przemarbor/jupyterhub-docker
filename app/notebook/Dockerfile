# Dockerfile for JupyterLab
# Jupyterhub version: 3.1.1

FROM jupyter/datascience-notebook:hub-3.1.1

# JupyterHub Version
ARG JUPYTERHUB_VERSION=3.1.1

USER root
RUN apt-get update && \
    apt-get install -y gnuplot automake octave libczmq-dev sbcl && \
    apt-get clean

# Install packages
RUN pip3 install --no-cache \
    jupyterlab-language-pack-pl-PL \
    octave_kernel && \
    export OCTAVE_EXECUTABLE=$(which octave)

ENV MaximaPath=/opt/maxima
RUN mkdir -p ${MaximaPath} && \
    git clone https://git.code.sf.net/p/maxima/code ${MaximaPath} && \
    cd ${MaximaPath} && \
    ./bootstrap && \
    ./configure --enable-sbcl --prefix=/usr/local --enable-quiet-build && \
    make install && \
    rm -rf ${MaximaPath} && \
    apt-get -q -y remove python3 autoconf automake make vim git curl && \
    apt-get -q -y clean && \
    apt-get -q -y autoclean && \
    rm -rf /var/lib/apt/lists/* /var/log/dpkg.log
USER jovyan
# Install maxima
RUN git clone https://github.com/robert-dodier/maxima-jupyter.git ${HOME}/maxima-jupyter
WORKDIR ${HOME}/maxima-jupyter

RUN export PYTHON_SITE=$(python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])') && \ 
	mkdir -p ${PYTHON_SITE}/notebook/static/components/codemirror/mode/maxima/ && \ 
	cp maxima.js ${PYTHON_SITE}/notebook/static/components/codemirror/mode/maxima/ 
	# && \ 
#	patch ${PYTHON_SITE}/notebook/static/components/codemirror/mode/meta.js codemirror-mode-meta-patch
# && \
# cp maxima_lexer.py ${PYTHON_SITE}/pygments/lexers/ && \
# patch ${PYTHON_SITE}/pygments/lexers/_mapping.py pygments-mapping-patch
RUN curl -kLO https://beta.quicklisp.org/quicklisp.lisp && \
    sbcl --non-interactive --load quicklisp.lisp --load docker-install-quicklisp.lisp && \
    maxima --batch-string="load(\"load-maxima-jupyter.lisp\");jupyter_install();"

WORKDIR ${HOME}
