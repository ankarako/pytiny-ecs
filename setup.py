import setuptools

setuptools.setup(
	name="pyapp",
	version="0.1.0",
	author="Antonis Karakottas",
	description="A small library for creating GUI aplications in python.",
	classifiers=["Programming Language :: Python :: 3", "License :: MIT", "Operating System :: OS Independent"],
	python_requires=">=3.7",
	install_requires=[
        "imgui[full]",
	],
)