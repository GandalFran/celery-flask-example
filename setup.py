from setuptools import setup
from config import APP_NAME, VERSION, DESCRIPTION, AUTHOR, AUTHOR_EMAIL, LICENSE

# requirements
flask_requirements = ['Flask==1.1.1', 'flask_restplus==0.13.0', 'flask_cors==3.0.8', 'werkzeug==0.16.1']
celery_requirements = ['celery==4.4.0', 'gevent==1.5a3']

requirements = flask_requirements + celery_requirements
setup(
    name=APP_NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    url="https://localhost:8080",
    packages=[],
    install_requires=requirements
)