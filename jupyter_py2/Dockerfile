# Choose your desired base image
FROM jupyter/scipy-notebook:latest

# Create a Python 2.x environment using conda including at least the ipython kernel
# and the kernda utility. Add any additional packages you want available for use
# in a Python 2 notebook to the first line here (e.g., pandas, matplotlib, etc.)
RUN conda create --quiet --yes -p $CONDA_DIR/envs/python2 \
	python=2.7 ipython ipykernel kernda \
	imageio \
	matplotlib \
	pandas \
	mne \
	numpy \
	Pillow \
	cvxopt \
	xmltodict && conda clean -tipsy

USER root

RUN apt-get update && apt-get --show-progress --no-install-recommends -y install python-pip python-tk

# Create a global kernelspec in the image and modify it so that it properly activates
# the python2 conda environment.
RUN $CONDA_DIR/envs/python2/bin/python -m ipykernel install &&  $CONDA_DIR/envs/python2/bin/kernda -o -y /usr/local/share/jupyter/kernels/python2/kernel.json

# install additional package
RUN $CONDA_DIR/envs/python2/bin/python -m pip install biosppy

USER $NB_USER
