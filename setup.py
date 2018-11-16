from setuptools import find_packages, setup


def get_requirements(env):
    with open(f"requirements/{env}.txt", "r") as fp:
        return [
            x.strip()
            for x in fp.read().split("\n")
            if x and not x.startswith("#") and not x.startswith("-r ./base")
        ]


install_requires = get_requirements("base")
develop_requires = get_requirements("develop")
product_requires = get_requirements("product")

setup(
    name="django_blog",
    version=0.1,
    url="https://blog.jasonqiao36.cc/",
    author="Jason Qiao",
    author_email="jasonqiao36@gmail.com",
    description="Blog system based on Django",
    package_dir={"": "django_blog"},
    packages=find_packages("django_blog"),
    zip_safe=False,
    include_package_data=True,
    scripts=["manage.py"],
    install_requires=install_requires,
    extras_require={"develop": develop_requires, "product": product_requires},
    classifiers=[
        "Framework :: Django",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
    ],
)
