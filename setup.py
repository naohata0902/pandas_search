from setuptools import setup, find_packages

def requirements_from_file(file_name):
    return open(file_name).read().splitlines()

setup(
    name='pandas_search',
    version='0.1.0',
    packages=find_packages(),
    # packages=find_packages("pandas_search"),
    # package_dir={"": "pandas_search"},
    install_requires=requirements_from_file('requirements.txt'),

    author='N Hatakeyama',
    
)