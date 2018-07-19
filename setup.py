from setuptools import find_packages, setup

packages = find_packages('django_blog')

setup(
    name='django_blog',
    version=0.1,
    url='https://blog.jasonqiao36.cc/',
    author='Jason Qiao',
    author_email='jasonqiao36@gmail.com',
    description='Blog system based on Django',
    packages=packages,
    package_dir={'': 'django_blog'},
    include_package_data=True,
    scripts=['django_blog/manage.py'],
    install_requires=[
        'django==2.0.5',
        'coreapi==2.3.3',
        'Django==2.0.5',
        'django-autocomplete-light==3.2.10',
        'django-redis==4.9.0',
        'django-rest-framework==0.1.0',
        'Markdown==2.6.11',
        'PyMySQL==0.8.1',
    ],
    zip_safe=False,
)
