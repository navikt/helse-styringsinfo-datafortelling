.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))

root_dir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

help:
	@echo "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

bootstrap: # Setter opp miljø for quarto-rendring
	poetry --version || brew install poetry
	quarto --version || brew install quarto@1.3.450

poetry-update:
	stat pyproject.toml || poetry init --no-interaction --name styringsinfo-datafortelling --description "" --author NAV -l MIT
	cat requirements.txt | xargs poetry add --python=3.11
	awk '/^packages/{print "packages = []"; next} 1' pyproject.toml > tmpfile && mv tmpfile pyproject.toml # 'poetry install' feiler hvis det ligger noe i packages.
	poetry install

login: # Sjekker om man er autentisert mot gcloud og logger inn hvis ikke
	gcloud auth print-identity-token >/dev/null 2>&1 || gcloud auth login --update-adc # Reduserer antall ganger man har glemt å logge på

env: # Slipper feilmelding fordi .env-fil mangler
	stat .env || cp env.example .env 

setup: bootstrap poetry-update env ## Setter opp miljø for å rendre datafortellingen

render: setup login ## Rendrer quarto datafortelling til index.html og åpner i nettleser
	poetry run quarto render index.qmd && open index.html

preview: setup login  ## Rendrer quarto datafortelling til lokal webserver ved å lytte på endringer i index.qmd 
	poetry run quarto preview index.qmd

preview_no_execute: setup login  ## Samme som preview, men kjører ikke python-koden
	poetry run quarto preview index.qmd --no-execute