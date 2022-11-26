#!/bin/bash
CURRENT_DIR=$PWD
echo $PRJ_WD
mkdir -p $PRJ_WD
cd $PRJ_WD
mkdir ./dense
touch ./dense/fused.ply
cd $CURRENT_DIR
