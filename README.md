![circle-ci](https://travis-ci.com/labhackercd/new-wikilegis.svg?branch=dev) ![python3-badge](https://img.shields.io/badge/python-django-green.svg) ![enter image description here](https://img.shields.io/badge/license-GPLv3-blue.svg) 

# wikilegis
> Collaborative editing of legislative texts.

## Installation
First of all, you need to install [pipenv](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv) and [npm](https://www.npmjs.com/get-npm). After install these dependencies you can run the follow commands:

```
pipenv install
npm install
pipenv run src/manage.py collectstatic_js_reverse
```

## Running

```
pipenv run src/manage.py migrate
pipenv run src/manage.py compilemessages
pipenv run src/manage.py runserver
```

## Support

Fell free to create any issue on this repository and contact the team responsible to maintain this project here on GitHub (@msfernandes, @erivanio, @cfviotti and @pettalves) or via email: labhacker@camara.leg.br.

## Contributing
1. Fork of this repository
2. Write your code
3. Create a Pull Request
4. Our team will review your PR and merge as soon as possible!

## License
This project is under GPLv3 License

