# Datafortelling - styringsinformasjon for sykepengeløsningen

En naisjobb for å genere en quarto-basert datafortelling med styringsinformasjon.

## Utvikling

Anbefaler å bruke VS Code med Quarto extension for utvikling. 

Om man bare vil rendre [index.qmd](index.qmd) til [index.html](index.html) lokalt kan man forsøke:

```shell
make render        # Kun testet på MacOS
```

Opprett/endre [.env](.env)-filen (se [env.example](env.example)) med annen prosjekt-id hvis du trenger å teste mot annet miljø enn dev.
