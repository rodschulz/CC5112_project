#/bin/bash

files=$1*
for f in $files
do
  echo 'Processing' $f
  python sampler.py $f
done