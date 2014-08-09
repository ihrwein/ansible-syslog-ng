# Syslog-ng Ansible role
A role for managing syslog-ng on your computers.

## Requirements & Dependencies

### Ansible
It was tested on the following versions:
 * 1.7.0

### Operating systems

Currently the module was only tested on Ubuntu Trusty (14.04 LTS), but it should work on other Debian based systems, too.

## Operating modes

It supports the following modes:

 * `local`: all logs are stored on the local machine
 * `client`: all logs are sent to one or more syslog servers
 * `server`: receives logs and stores them on its local filesystem
 * `manual`: a stock Debian `syslog-ng.conf`, you can tweak it as you want

The default mode is `local`.

## Variables

This module uses YAML syntax to define variables. You must explicitly care about the quotation and some values.

If you assign `yes` or `no` to a variable, YAML treats it as boolean value. In most cases you doesn't want this, so place these words between single or double quotes: `'yes'`, `'no'`.

When you want to write a string into `syslog-ng.conf` (for example a hostname), you must double qoute it (`'"secure.example.com"'`) to get the right string in the config (`"secure.example.com"`). You can swap the inner an outer quotation marks.

You can find examples in the `defaults/main.yml` file.

### Global variables

 * `syslog_ng_mode`: `local`|`client`|`server`|`manual` defines the operating mode.
 * `syslog_ng_config_options`: a dictionary containing [global options](http://www.balabit.com/sites/default/files/documents/syslog-ng-ose-3.5-guides/en/syslog-ng-ose-v3.5-guide-admin/html-single/index.html#reference-options).
 * `syslog_ng_config_version`: float, which configuration version you want to use
 * `syslog_ng_config_includes`: list of file names, which will be included at the beginning of `syslog-ng.conf`
 * `syslog_ng_config_dir`: string, where are the config files
 * `syslog_ng_config_file`: string, the path to `syslog-ng.conf`
 * `syslog_ng_config_include_from_conf_d`: boolean, you can include all files from `conf.d` into `syslog-ng.conf`. This statement is at the end of it, so be careful do not include the same files multiple times by using this and `syslog_ng_config_includes` variables
 * `syslog_ng_group`: the owner group of `syslog-ng.conf`
 * `syslog_ng_user`: the owner user of `syslog-ng.conf`

### Mode specific variables
#### Local

In this mode syslog-ng collects all of your local logs and writes them into files on your local filesystem. It uses the `system()` and `internal()` sources. For most systems, this is the default configuration.

 * `syslog_ng_local_dest_dir`: the base directory to store files

#### Client

In this mode, syslog-ng collects all logs from your system and sends them to one or more syslog-ng servers.

 * `syslog_ng_client_destinations`: target servers in the following format:

```yaml
syslog_ng_client_destinations:
  - "candrop.example.com":
      proto: udp
      port: 1234
      filters:
        - filter_name_1
        - filter_name_2
  - "secure.example.com":
      proto: tls
      port: 10514
      ca_dir: /opt/syslog-ng/etc/syslog-ng/ca.d
      key_file: /opt/syslog-ng/etc/syslog-ng/key.d/client.key
      cert_file: /opt/syslog-ng/etc/syslog-ng/cert.d/client_cert.pem
  - "tcp.example.com":
      proto: udp
      port: 1234
 ```
***NOTE:*** each item in `syslog_ng_client_destinations`is a dictionary with only one key - the actual hostname. The `proto`, `port`, etc. fields are not on the same level, as the hostname!

***NOTE:*** you have to define all filter statements before you reference them. One way of doing this is to add a filename into `syslog_ng_config_includes` list, which makes syslog-ng include the contents of this file at be beginning of `syslog-ng.conf`. Be aware, that you must disable the `syslog_ng_config_include_from_conf_d` in this case, because it can cause double includes.

#### Server

 * `syslog_ng_server_dest_dir`: the logfiles will be placed under this directory
 * `syslog_ng_server_sources`: its structure is same as  `syslog_ng_client_destinations`, but it defines sources
 ```yaml
 syslog_ng_server_sources:
   - "candrop.example.com":
       proto: udp
       port: 1234
       filters:
         - f_error
         - f_kern
   - "secure.example.com":
       proto: tls
       port: 10514
       ca_dir: /opt/syslog-ng/etc/syslog-ng/ca.d
       key_file: /opt/syslog-ng/etc/syslog-ng/key.d/client.key
       cert_file: /opt/syslog-ng/etc/syslog-ng/cert.d/client_cert.pem
   - "tcp.example.com":
       proto: udp
       port: 1234
 ```
 * `syslog_ng_server_file_macro`: you can sort out  messages into different files by using this parameter. The files will be placed under `syslog_ng_server_dest_dir`. You can find more information in the [Syslog-ng Admin Guide](http://www.balabit.com/sites/default/files/documents/syslog-ng-ose-3.5-guides/en/syslog-ng-ose-v3.5-guide-admin/html-single/index.html#configuring-macros)

 ```yaml
   syslog_ng_server_file_macro: $YEAR.$MONTH.$DAY/$HOST.log
 ```

#### Manual

This role was designed with simplicity in mind to be easy to use and provide the most basic functionalities without manually touching `syslog-ng.conf`.

For that very reason you can use this mode to use `syslog-ng` in the normal way, by manually defining sources, destination, filters and so on.

The `templates/manual.j2` file is a copy of a stock Debian `syslog-ng.conf`. You can use Jinja expressions in it and you have access to the defined variables as well. Tweak it as you want, by applying this role it will be automatically 'copied' to your server.

## Development
### Contribution
If you find a bug, please open an issue on [GitHub](https://github.com/ihrwein/ansible-syslog-ng/issues).

If you want to hack some features into this role, please open an issue and we will talk about that.
