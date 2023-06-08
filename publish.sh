#!/bin/bash
set -e

quarto render index.qmd

curl -X PUT -F index.html=@index.html \
    "https://${ENV}/quarto/update/${QUARTO_ID}" \
    -H "Authorization:Bearer ${NADA_TOKEN}"