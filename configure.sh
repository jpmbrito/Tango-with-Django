#!/bin/bash

export PYTHONPATH=$(echo "import site; print (site.getsitepackages()[0])" | python)
export PYTHONPATH=$PYTHONPATH:$PYTHONPATH/django/bin/

echo $PYTHONPATH
