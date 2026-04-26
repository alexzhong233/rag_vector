from setuptools import setup, find_packages

setup(
    name="rag_vector",
    version="1.0.0",
    description="RAG System with pgvector",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary>=2.9.9",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "sentence-transformers>=2.2.2",
        "openai>=1.3.0",
    ],
    extras_require={
        "anthropic": ["anthropic>=0.7.0"],
        "api": ["fastapi>=0.104.0", "uvicorn>=0.24.0"],
        "dev": ["pytest>=7.4.0", "pytest-asyncio>=0.21.0"],
    },
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "rag=main:main",
        ],
    },
)
