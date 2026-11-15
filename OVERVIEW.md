# JupyterLab with the scientific Python stack

## What it is

A JupyterLab workspace that runs on a remote machine and opens in your browser,
with the scientific Python packages most people reach for already installed:
pandas, NumPy and SciPy, scikit-learn, statsmodels, matplotlib, seaborn,
Bokeh and Altair, Dask, SymPy, and more. It is the same set as the widely used
Jupyter Docker Stacks "scipy-notebook", adapted for shared research computing
systems, so that one image can serve many HPC centers while each person's
session stays their own.

The session opens in the directory it was started from, so your notebooks and
data are there, and what you create is saved back to the same place. Save your
work there: depending on how the app is set up, your home directory may be
fresh for each session.

## Use cases

- Data analysis, statistics and plotting without installing anything locally.
- Teaching and workshops: every participant gets the same packages at the same
  versions.
- Larger-than-memory or parallel work with Dask, on a machine bigger than your
  own.
- A starting point for a Jupyter app with your own packages: copy it and change
  the package list.

## What's included

- JupyterLab, with a terminal and a Git panel.
- The scientific Python packages listed above, at fixed versions.
- Exporting notebooks to PDF, LaTeX in plots, and animations.
- A private, single-user session, reached through a link only you have.

Not included: installing packages while a session runs. To add a package, it is
added to the app's package list and a new version is built.

## Where it can run

- **Through a science gateway**, which starts the session and gives you the link.
- **On a research cluster**, through Apptainer/Singularity, as an interactive job.
- **On your own computer**, through Docker.

It runs without special privileges and uses a single network port.

## Getting started

Through a gateway, open the link you are given. JupyterLab appears in the
directory the session started in; work and save there. Choose File > Shut Down
when you are finished.
