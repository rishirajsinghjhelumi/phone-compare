
from setuptools import setup

setup(
    name = 'Phone Compare',
    version = '1.0',
    long_description = __doc__,
    packages = ['PhoneCompare'],
    include_package_data = True,
    zip_safe = False,
    install_requires = [
    	'flask',
    	'flask-script',
    	'WTForms',
    	'flask-sqlalchemy',
    	'mongoengine',
    	'flask_mongoengine',
    	'flask-script',
    	'Flask-WTF'
    ]
)