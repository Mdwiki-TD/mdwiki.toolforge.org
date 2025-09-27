#!/bin/bash
webservice stop
webservice --backend=kubernetes php8.2 start
rm *.out

