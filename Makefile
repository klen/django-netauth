MODULE=django-netauth

clean:
	sudo rm -rf build dist django_netauth.egg-info
	find . -name "*.pyc" -delete

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
