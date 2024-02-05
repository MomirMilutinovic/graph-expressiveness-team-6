from setuptools import setup, find_packages

setup(
    name='html-datasource',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'datasources': [
            'html = src.html_datasource.implementation:HtmlDataSource',
        ],
    },
)