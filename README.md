<!-- markdownlint-disable MD041-->
<p align="center">
    <a href="#readme">
        <img alt="WeatherWiz logo" src="https://raw.githubusercontent.com/pykong/weatherwiz/main/docs/header.png">
        <!-- Logo credits: Benjamin Felder -->
    </a>
</p>
<p align="center">
    <a href="#readme"><img alt="PlaceholderBadge" src="https://badgen.net/static/PyVersion/3.10/purple"></a>
    <a href="#readme"><img alt="PlaceholderBadge" src="https://badgen.net/static/Code-Quality/A+/green"></a>
    <a href="#readme"><img alt="PlaceholderBadge" src="https://badgen.net/static/Ruff/OK/green"></a>
    <a href="#readme"><img alt="PlaceholderBadge" src="https://badgen.net/static/Coverage/0.0/gray"></a>
    <a href="#readme"><img alt="PlaceholderBadge" src="https://badgen.net/static/MyPy/78.0/blue"></a>
    <a href="#readme"><img alt="PlaceholderBadge" src="https://badgen.net/static/Docs/0.0/gray"></a>
    <a href="https://github.com/pykong/weatherwiz/main/LICENSE">
        <img alt="License" src="https://badgen.net/static/license/MIT/blue">
    </a>
    <a href="#readme"><img alt="PlaceholderBadge" src="https://badgen.net/static/Build/1.0.0/pink"></a>
    <a href="#readme"><img alt="PlaceholderBadge" src="https://badgen.net/static/stars/★★★★★/yellow"></a>
</p>
<p align="center">
    <a href="#readme">
        <img alt="Example Dialog" src="https://github.com/pykong/weatherwiz/blob/main/docs/frontend.gif?raw=true">
    </a>
</p>

# WeatherWiz

WeatherWiz is a chatbot for weather forecasts.
It is built with [Rasa](https://rasa.com/), Python and love ❤️ and proudly **features**:

- a fancy frontend build with [chatroom.js](https://github.com/scalableminds/chatroom)
- using free APIs (_no signup or API key required_):
  - **real weather data** from [Bright Sky](https://brightsky.dev/docs/#/) API
    - forecasts up to seven days
    - historical data from 01.01.2010
  - geocoding via [Nominatim](https://nominatim.org/) API
  - user IP address as a location fallback via [ipinfo.io](https://ipinfo.io/) API
- slots for place and time for keeping conversation context
- a [dateparser](https://dateparser.readthedocs.io/en/latest/) for date and time extraction
- high test coverage via Pytest and Rasa's tests
- full Dockerization

## Getting started

To start WeatherWiz you will need:

- a working [Docker engine](https://docs.docker.com/engine/install/)
- Internet access (for setup and API access)
- at least 16GB RAM (32GB recommended)

Talking to WeatherWiz is as easy as:

1. Clone the project
2. Open a shell in the project folder
3. In the shell, run `docker compose up`
4. Open [localhost:8000](http://localhost:8000) in your browser
5. Enjoy talking to WeatherWiz... 🙂

## Contributing

WeatherWiz suggests the following development setup:

1. **Docker** to run the application
2. **Poetry** for dependency management
3. **Ruff** for formatting and linting
4. A type checker, preferably [pyright](https://github.com/microsoft/pyright)
5. **Pytest** for unit testing

Configuration is located in the `pyproject.toml`, at the root of the project.

To contribute:

1. Fork this repository
2. Do your changes, including:
   - test coverage
   - documentation
3. Open a PR

You may also feel free to open any issue.

## Current limitations

- WeatherWiz will only answer questions regarding rain, temperature and wind
- answer format remains generic
- failure of API access is not handled gracefully

## Links

- [dateparser](https://dateparser.readthedocs.io/en/latest/)
- [DateparserEntityExtractor](https://rasahq.github.io/rasa-nlu-examples/docs/extractors/dateparser/)
- [chatroom.js](https://github.com/scalableminds/chatroom)
- [Bright Sky](https://brightsky.dev/docs/#/)
- [Nominatim](https://nominatim.org/)
- [ipinfo.io](https://ipinfo.io/)
