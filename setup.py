from setuptools import setup, find_packages

setup(
    name="social-media-ai-agent",
    version="1.0.0",
    description="AI-powered social media management agent system",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
        "flask>=2.0.0",
    ],
    python_requires=">=3.9",
) 