from setuptools import find_packages, setup

packages = find_packages('django_blog')

setup(
    name='django_blog',
    version=0.1,
    url='https://www.jasonqiao36.cc/',
    author='Jason Qiao',
    author_email='jasonqiao36@gmail.com',
    description='Blog system based on Django',
    packages=packages,
    package_dir={'': 'django_blog'},
    include_package_data=True,
    scripts=['django_blog/manage.py'],
    install_requires=['django==2.0.5'],
    zip_safe=False,
)
