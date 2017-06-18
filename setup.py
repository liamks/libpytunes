from setuptools import setup, find_packages

setup(
    name="libpytunes",
    version="1.5.2",
    license='MIT',
    author="Liam Kaufman",
    author_email="",
    url="https://github.com/liamks/libpytunes",
    description="Python Itunes Library parser",
    long_description=open("README.md").read(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=[]
    )
