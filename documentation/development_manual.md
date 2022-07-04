# Development manual

## Running the development locally

The project has poetry as dependency management. Most development can thus be done using `poetry shell`-command locally. This can probably be done with just Docker too. Running the website locally work with `./gunicorn.sh`-command.

## Website design

The website is using some University of Helsinki html-templates and styling that are taken from the [university styling guide](https://static.helsinki.fi/ds/). The downloaded stylesheets in `layout.html` are from the guide. The styling guide was in alpha-stage at the moment of development so a lot of styling was done by hand as some of the styling from the guide didn't work. It is possible that something will change in the guide in the future so it might break something on the website.

## Local data-folders

The local `data` and `user_templates` -folders contain data just for local testing and development. When using the Docker volumes on the server, the data inside these local folders won't be visible on the website, as only data added to the server folders will be shown there.

## Tests

Executing `pytest src` runs the UI before the tests as defined in `conftest.py`. This is because the `test_routes.py` tests whether the website works and the UI needs to be executed before that.

## Library versions

The libraries used for development and their version numbers that have worked correctly during the development. The list is from poetry dependencies:

```bash
[tool.poetry.dependencies]
python = "^3.8"
invoke = "^1.7.1"
Flask = "^2.1.2"
python-dotenv = "^0.20.0"
gunicorn = "^20.1.0"
gfapy = "^1.2.3"
beautifulsoup4 = "^4.11.1"
requests = "^2.28.0"

[tool.poetry.dev-dependencies]
pytest = "^7.1.2"
coverage = "^6.3.3"
pylint = "^2.13.9"
pytest-dotenv = "^0.5.2"
```

## Ohtuprojekti staging server

If future developers use the [course staging server](https://github.com/UniversityOfHelsinkiCS/ohtup-staging), it only worked for us if all addresses had a `/hggd`-prefix added in front of them, as the staging server needs the server to be run from a subfolder rather than just from the root address as in production server. In this case, also the production server addresses change. At the moment the prefix is removed so the server address looks nocer.
