#!/bin/bash
set -e

quarto render index.qmd

curl -v -o - -X PUT -F index.html=@index.html \
    "https://${NADA_URL}/quarto/update/${QUARTO_ID}" \
    -H "Authorization:Bearer ${NADA_TOKEN}"