from setuptools import setup, find_packages

setup(
    name='html_datasource',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'datasources': [
            'html_datasource = html_datasource.html_data_source:HtmlDataSource',
        ],
    },
)