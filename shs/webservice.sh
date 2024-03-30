#!/bin/bash
webservice stop
webservice --backend=gridengine --release buster start
rm *.out

