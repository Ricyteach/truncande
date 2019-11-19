from setuptools import setup

setup(
    name="truncande",
    version="0.1",
    packages=["truncande"],
    extras_require=dict(dev=["pytest",]),
    entry_points="""
    [console_scripts]
    truncande=truncande.cli:main
    """,
    url="https://github.com/Ricyteach/truncande",
    license="MIT",
    author="Rick Teachey",
    author_email="ricky@teachey.org",
    description="Truncate CANDE output files",
)
