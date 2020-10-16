import setuptools

setuptools.setup(name="autossh",
        version="1.3.0",
        description="Auto-SSH toolkits",
        url="https://www.github.com/anticpp/autossh",
        author="supergui",
        author_email="supergui@live.cn",
        license="None",
        install_requires=['pexpect'],
        packages=setuptools.find_packages(),
        scripts=["bin/assh", "bin/apush", "bin/apull", "bin/acat"],
        include_package_data=True,
        zip_safe=False)
