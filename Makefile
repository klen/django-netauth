MODULE=django-netauth

clean:
	sudo rm -rf build dist django_netauth.egg-info
	find . -name "*.pyc" -delete
	find . -name "*.orig" -delete

install: remove _install clean

remove:
	sudo pip uninstall $(MODULE)

_install:
	sudo pip install -U .

register: _register clean

upload: _upload clean

_upload:
	python setup.py sdist upload

_register:
	python setup.py register

test:
	cd example_project && ./manage.py test main
