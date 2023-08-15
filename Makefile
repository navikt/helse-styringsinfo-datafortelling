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
	sed -i '/^packages/c\packages = []' pyproject.toml # 'poetry install' feiler hvis det ligger noe i packages.
	poetry install

render: bootstrap poetry-update ## Rendrer quarto datafortelling til index.html
	stat .env || cp env.example .env # Slipper feilmelding fordi .env-fil mangler.
	@gcloud --format=json auth list | jq --exit-status '.[] | select(.status == "ACTIVE")' || gcloud auth application-default login
	poetry run quarto render index.qmd && open index.html
