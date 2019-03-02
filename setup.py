from setuptools import setup

setup(name="autossh",
        version="0.1",
        description="Auto-SSH toolkits",
        url="https://www.github.com/anticpp/autossh",
        author="supergui",
        author_email="supergui@live.cn",
        license="None",
        packages=["autossh"],
        scripts=["bin/assh", "bin/ascp", "bin/apwd"],
        zip_safe=False)