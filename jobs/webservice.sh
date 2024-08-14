#!/bin/bash
webservice stop
webservice --backend=kubernetes php7.4 start
rm *.out

