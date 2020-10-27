Toolkits for convenient SSH.
=====================================

## Notice

Python2 is not supported.

## Install

`sudo pip3 install --root=/ .`

## Configuration

### Config

All configurations have default values, you don't have to create config file. Or you can create one at `~/.config/<module>/config.yaml`. Refer to \$repo`/config/<module>/config.yaml` for configuration detail.

### Host file
Add host file at `~/.config/autossh/hosts`. Refer to \$repo`/config/autossh/hosts`.

Formate:

```
host[:port][\[alias\]]     user    password
```

- host: Ip or hostname, required.
- port: Port, optional.
- alias: Alias name for host, optional.
- user: Login user, required. "None" for anonymous.
- password: Login password, required. "None" for anonymous.

## Toolkits

Run `-h` for help messages.

- assh
- apush
- apull
- acat
- qssh

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
