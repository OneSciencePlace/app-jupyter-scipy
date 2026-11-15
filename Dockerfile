# app-jupyter-scipy: JupyterLab with the scientific Python stack of the Jupyter
# Docker Stacks' scipy-notebook, adapted for shared research computing systems.
#
# You do not need to edit this file. To make your own image, change
# requirements.txt (Python packages) and, rarely, apt.txt (system packages):
# see README.md, "Make your own".
#
# Everything about the session -- the token gate, JupyterLab on a Unix socket,
# the private session directory, Dask secured per session -- comes from the
# base image, app-jupyter, pinned here by tag and digest.
FROM ghcr.io/onescienceplace/app-jupyter:4.6.3-osp3@sha256:d38fa80f090ef7edb1cc9fe6d20d7101bd35976b110e55cfcaf8e95561972491

# Your packages: requirements.txt, apt.txt (and session.d/, if you add one).
COPY . /tmp/osp/
RUN /app/osp/install.sh /tmp/osp

# Always the last RUN line: checks the image and removes what must not be in it.
RUN /app/osp/finish-build.sh
