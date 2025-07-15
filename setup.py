"""
Setup script for the Hyperchronal Framework research project.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hyperchronal-framework",
    version="0.1.0",
    author="PelicansPerspective",
    author_email="contact@pelicansperspective.org",
    description="Research tools for the Hyperchronal Framework unifying consciousness, cosmology, and quantum theory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PelicansPerspective/hyperchronal-framework",
    project_urls={
        "Bug Tracker": "https://github.com/PelicansPerspective/hyperchronal-framework/issues",
        "Documentation": "https://PelicansPerspective.github.io/hyperchronal-framework/",
        "Source": "https://github.com/PelicansPerspective/hyperchronal-framework",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
            "mypy",
            "jupyter",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
        ],
    },
    keywords="physics, quantum mechanics, cosmology, consciousness, theoretical physics",
)
