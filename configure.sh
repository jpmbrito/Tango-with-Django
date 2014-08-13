#!/bin/bash

export PYTHONPATH=$(echo "import site; print (site.getsitepackages()[0])" | python)

echo $PYTHONPATH
