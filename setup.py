from setuptools import setup, find_packages;

with open('README.md') as f:
    readme = f.read()

setup(
    name='ptls',
    version='0.0',
    description='Physical Therapy Clinic Location Scraper',
    long_description=readme,
    author='Roshan Giyanani',
    author_email='roshangiyanani@gmail.com',
    url='https://github.com/roshangiyanani/pt_location_scaper',
    license=license,
    packages=find_packages(exclude=('test', 'data'))
)