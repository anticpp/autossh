Toolkits for convenient SSH.
=====================================

## Install

`pip install .`

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

- apwd
    + Show password.


## TODO

- Fix escape character '\x1d' conflicted with `vim`.
- Remove `pexpect.py`.
- Publish to PyPI.
- Command line arguments.
    + -t timeout
