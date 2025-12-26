from setuptools import setup, find_packages

setup(
    name="student-risk-prediction",
    version="0.1.0",
    description="API for predicting student dropout risk",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.23.0",
        "pandas>=1.5.0",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.0",
        "pydantic>=2.0.0",
        "joblib>=1.3.0",
    ],
    python_requires=">=3.8",
)
