"""Packaging, so that the analysis can be installed with ``pip install -e .``"""

import setuptools

setuptools.setup(
    name="jpsi_analysis",
    version="0.1.0",
    description="J/psi to mu mu, 2023",
    author="",
    packages=setuptools.find_packages(include=["jpsi_analysis", "jpsi_analysis.*"]),
    package_data={
        "jpsi_analysis": [
            "configs/*.yaml",
            "configs/samples/*.yaml",
            "data/*",
        ],
    },
    include_package_data=True,
    python_requires=">=3.9",
)
