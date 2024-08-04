import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ok-script",
    version="0.0.160",
    author="ok-oldking",
    author_email="firedcto@gmail.com",
    description="Automation with Computer Vision for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ok-oldking/ok-script",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[
        'adbutils>=2.7.2',
        'numpy>=1.26.4',
        'PyDirectInput>=1.0.4',
        'pywin32>=306',
        'typing-extensions>=4.11.0',
        'PySide6>=6.7.0',
        'PySide6-Fluent-Widgets>=1.5.6',
        'psutil>=5.9.8',
        'opencv-python>=4.9.0.80',
        'ok-d3dshot>=0.1.5',
        'py7zr>=0.21.0',
        'wmi>=1.5.1'
    ],
    python_requires='>=3.6',
)
