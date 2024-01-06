setup(
    name="Dispatch-Portal",
    version="1.0.0",
    description="Application for connecting retailers with their clients for both marketing and communication",
    long_description=README.md,
    long_description_content_type="text/markdown",
    url="https://github.com/publicaddress/marketing",
    author="Eric Stevens",
    author_email="e.bst@pm.me",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: JavaScript :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["reader"],
    include_package_data=True,
    install_requires=[
        "installer_macOS.sh"
    ],
    entry_points={"console_scripts": ["Dispatch-Portal=source.Dispatch-Portal:main_loop"]},
)
