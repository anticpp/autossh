Toolkits for convenient SSH.
=====================================

## Notice

Python2 is not supported.

## Install

`pip3 install .`

## Configuration

### Config

Default configure file is `~/.config/autossh/config.yaml`. You can get a copy at `conf/config.yaml`.

### Host entry 
Put your login host to host entry file, which default path is `~/.autossh/hosts`. You can get a copy at `conf/hosts.demo`.

Formated as:

```
host[alias]     user    password
```

- host: Ip or hostname
- alias: An alias name of host
- user: Login user
- password: Login password

## Tools

Get help message by running with no argument.

- assh
    + Auto ssh.

- ascp
    + Auto scp.

- acat
    + Cat hosts.


## TODO

- Fix escape character '\x1d' conflicted with `vim`.
    + DONE
- Remove `pexpect.py`.
    + DONE
- Messy window size with `vim` or `man page`.
    + DONE
- Migrage to Py3
    + Done
- Publish to PyPI.
- Command line arguments.
    + -t timeout
- Add tool `apull`.
