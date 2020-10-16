Toolkits for convenient SSH.
=====================================

## Notice

Python2 is not supported.

## Install


`sudo pip3 install --root=/ .`

## Configuration

### Config

All configurations have a default value, or you can configure with configure file `~/.autossh/config.yaml`. Refer to \$repo/`conf/config.yaml`.


### Host entry 
Create a host entry file at `~/.autossh/hosts`. Refer to \$repo/`conf/hosts.demo`.

Formated as:

```
host[alias]     user    password
```

- host: Ip or hostname
- alias: An alias name of host
- user: Login user
- password: Login password

## Toolkits

- assh
- apush
- apull
- acat


## TODO

- Fix escape character '\x1d' conflicted with `vim`.
    + DONE
- Remove `pexpect.py`.
    + DONE
- Messy window size with `vim` or `man page`.
    + DONE
- Migrage to Py3
    + Done
- Default configuration.
    + DONE
- Publish to PyPI.
- Command line arguments.
    + -t timeout
- Add tool `apush` `apull`.
    + DONE
- Install exec to specified dir, etc `/usr/local/bin/`.
    + DONE
