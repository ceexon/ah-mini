"""Start and run app."""
from setuptools import setup, find_packages

setup(
    name="a-haven",
    version="0.1",
    py_modules=find_packages(),
    include_package_data=True,
    install_requires=[
            "Click",
            "requests",
            "halo",
            "pytest",
            "pytest-cov>=2.4.0,<2.6",
            "coverage",
            "coveralls",
            "inquirer",
    ],
    entry_points="""
        [console_scripts]
        ah=my_commands:main
        """,
)
