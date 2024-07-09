#!/bin/bash


cp -rn /data/project/mdwiki/public_html/Translation_Dashboard /data/project/medwiki/public_html -v
cp -rn /data/project/mdwiki/confs /data/project/medwiki -v
cp -rn /data/project/mdwiki/shs /data/project/medwiki -v
cp -rn /data/project/mdwiki/*.yaml /data/project/medwiki -v
cp -rn /data/project/mdwiki/user-config.py /data/project/medwiki -v
cp -rn /data/project/mdwiki/ux.py /data/project/medwiki -v



cp -ru /data/project/mdwiki/public_html /data/project/medwiki -v


cp -ru /data/project/mdwiki/public_html/bots/*.php /data/project/medwiki/public_html/bots -v
cp -ru /data/project/mdwiki/public_html/*.php /data/project/medwiki/public_html -v
cp -ru /data/project/mdwiki/pybot/newupdater /data/project/medwiki/pybot -v
cp -ru /data/project/mdwiki/pybot/wprefs /data/project/medwiki/pybot -v



cp -ru /data/project/mdwiki/public_html/Translation_Dashboard/*.php /data/project/medwiki/public_html/Translation_Dashboard -v
cp -ru /data/project/mdwiki/public_html/Translation_Dashboard/enwiki/*.php /data/project/medwiki/public_html/Translation_Dashboard/enwiki -v
