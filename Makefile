.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))

root_dir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

help:
	@echo "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

bootstrap: # Setter opp miljø for quarto-rendring
	poetry --version || brew install poetry
	quarto --version || brew install quarto

poetry-update:
	stat pyproject.toml || poetry init --no-interaction --name styringsinfo-datafortelling --description "" --author NAV -l MIT
	cat requirements.txt | xargs poetry add
	awk '/^packages/{print "packages = []"; next} 1' pyproject.toml > tmpfile && mv tmpfile pyproject.toml # 'poetry install' feiler hvis det ligger noe i packages.
	poetry install

render: bootstrap poetry-update ## Rendrer quarto datafortelling til index.html
	stat .env || cp env.example .env # Slipper feilmelding fordi .env-fil mangler.
	gcloud auth print-identity-token >/dev/null 2>&1 || gcloud auth login --update-adc # Reduserer antall ganger man har glemt å logge på
	poetry run quarto render index.qmd && open index.html

preview: bootstrap poetry-update ## Rendrer quarto datafortelling til lokal webserver ved å lytte på endringer i index.qmd 
	stat .env || cp env.example .env # Slipper feilmelding fordi .env-fil mangler.
	gcloud auth print-identity-token >/dev/null 2>&1 || gcloud auth login --update-adc # Reduserer antall ganger man har glemt å logge på
	poetry run quarto preview index.qmd