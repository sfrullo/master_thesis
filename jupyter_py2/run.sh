#/bin/bash

PWD=`pwd`

source $PWD/setenv.sh

echo $EMOSM_NOTEBOOK_DIR
echo $EMOSM_EXPORT_DIR

#sudo docker run -it \
#    -p 8888:8888 \
#    --user root \
#    -e CHOWN_EXTRA_OPTS='-R' \
#    -e CHOWN_HOME=yes \
#    -e CHOWN_EXTRA="/home/TesiCastellani/notebook,/home/TesiCastellani/export" \
#    -e NB_USER=TesiCastellani \
#    -w /home/TesiCastellani \
#    -v $EMOSM_NOTEBOOK_DIR:/home/TesiCastellani/notebook \
#    -v $EMOSM_EXPORT_DIR:/home/TesiCastellani/export \
#    jupyter-py2:latest

sudo docker run -it \
    -p 8888:8888 \
    -v $EMOSM_NOTEBOOK_DIR:/home/jovyan/work \
    -v $EMOSM_EXPORT_DIR:/home/jovyan/export \
    -v $EMOSM_PACKAGE_DIR:/home/jovyan/emosm \
    -v $DATASET_DIR:/home/jovyan/Dataset \
    jupyter-py2:latest
