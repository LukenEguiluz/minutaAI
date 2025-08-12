#!/usr/bin/env python3
"""
Setup script for MinutaAI
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="minutaai",
    version="1.0.0",
    author="MinutaAI Team",
    author_email="contact@minutaai.com",
    description="Aplicación web para transcripción automática de audio y video usando Whisper AI",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/MinutaAI",
    project_urls={
        "Bug Tracker": "https://github.com/tu-usuario/MinutaAI/issues",
        "Documentation": "https://github.com/tu-usuario/MinutaAI#readme",
        "Source Code": "https://github.com/tu-usuario/MinutaAI",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=6.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "minutaai=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/*", "static/*"],
    },
    keywords="transcription, whisper, audio, video, flask, ai",
    zip_safe=False,
)
