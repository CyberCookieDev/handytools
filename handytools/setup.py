from setuptools import setup

setup(
    name="handytools",
    version="0.1",
    description="A hub you can add your Python scripts, that has a few preloaded for you.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",  # Replace with the license you're using
        "Operating System :: Windows",
    ],
    python_requires=">=3.6",
    install_requires=[
        "colorama",
        "Send2Trash",
        "black",
        "psutil",
        "rich",
        "screeninfo",
    ],
)
