#!/bin/bash

. tests/common.sh

for i in {client,server,manual,local}; do
    MODE="${i}_mode"
    assert_zero_retcode ansible-playbook -i tests/inventory -e roles_path=$roles_path tests/${MODE}.yml --syntax-check
    assert_zero_retcode bash tests/pre/${MODE}.sh
    assert_zero_retcode ansible-playbook -i tests/inventory -e roles_path=$roles_path tests/${MODE}.yml --connection=local --sudo
    assert_zero_retcode bash tests/post/${MODE}.sh
    assert_zero_retcode cat /etc/syslog-ng/syslog-ng.conf
done
