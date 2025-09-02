"""
Setup script for financial-ai-assistant-dashboard Financial Dashboard
"""
from setuptools import setup, find_packages

APP_NAME = 'financial-dashboard'
VERSION = "1.0.0"
AUTHOR = 'Felipe Ferreira de Carvalho'
EMAIL = "felipefcnano@gmail.com"
SHORT_DESCRIPTION = "Integrated Financial Dashboard with AI Assistant for REXP and DIPD Analysis"
LDESCRIPTION_CONTENT_TYPE = "text/markdown"
MAIN_URL = "https://github.com/felipe0fc/financial-ai-assistant-dashboard.git"
PROJECT_URLS = {
        "Bug Reports": "https://github.com/felipe0fc/financial-ai-assistant-dashboard/issues",
        "Source": "https://github.com/felipe0fc/financial-ai-assistant-dashboard",
    }
CLASSIFIERS = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ]
PYTHON_MIN_VERSION = ">=3.8"
ENTRY_POINTS = {
        "console_scripts": [
            "financialai=app:main",
            "financialai-web=app:main",
            "financialai-cli=app:main",
        ],
    }
KEYWORDS = [
        "financial", "dashboard", "ai", "analysis", "rexp", "dipd", 
        "llm", "anthropic", "plotly", "dash", "business-intelligence"
    ]
def read_readme():
    """Read README.md file for long description"""
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "Financial Dashboard - Integrated Analysis System for REXP and DIPD companies"

def read_requirements():
    """Read requirements from requirements.txt"""
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        # Fallback requirements if requirements.txt doesn't exist
        return [
            "pandas>=2.3.2",
            "dotenv>=0.9.9",
            "pdfplumber>=0.11.7",
            "anthropic>=0.64.0",
            "dash>=3.2.0",
            "plotly>=6.3.0",
        ]

setup(
    name=APP_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=SHORT_DESCRIPTION,
    long_description=read_readme(),
    long_description_content_type=LDESCRIPTION_CONTENT_TYPE,
    url=MAIN_URL,
    project_urls=PROJECT_URLS,
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    python_requires=PYTHON_MIN_VERSION,
    install_requires=read_requirements(),
        entry_points=ENTRY_POINTS,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=KEYWORDS,
    platforms=["any"],
)