function assert_zero_retcode {
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        exit 1
    fi
    return $status
}


