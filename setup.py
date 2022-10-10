import setuptools

setuptools.setup(
	name="tiny-ecs",
	version="1.0.0",
	author="Antonis Karakottas",
	description="A small library for implementing an Entity-Component-System structure.",
	classifiers=["Programming Language :: Python :: 3", "License :: MIT", "Operating System :: OS Independent"],
	python_requires=">=3.7",
	install_requires=[
        "imgui[full]",
	],
)