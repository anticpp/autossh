Toolkits for convenient SSH.
=====================================

## Install

Run `sh install`. 

Tools will be installed at `~/bin/`, you should set this directory to your `$PATH` environment.

## Tools

Get help message by running with no argument.

- assh
    + Auto ssh.

- ascp
    + Auto scp.

- apwd
    + Show password.

## Configuration

### Host entry 
The default host entry file path is `~/.autossh/hosts`. You can configure line of a hostinfo as format:

```
host[alias]     user    password
```

- host: Ip or hostname
- alias: An alias name of host
- user: Login user
- password: Login password


Here is an example.

```
## Commet
192.168.0.1  root    password1
192.168.0.2  root    password2          ## Commet
192.168.0.3[dev3]  root    password3    ## Commet
192.168.0.4[dev4]  root    password4

```

## TODO

- Fix escape character '\x1d' conflicted with `vim`.
- Remove `pexpect.py`.
- Support pip install.
