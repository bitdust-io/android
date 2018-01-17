#!/bin/sh

SRC="./.bitdust/src"
VENV="./.bitdust/venv_deploy"
VENVSRC="./.bitdust/venv_src"

PYTHONINTERPRETATOR="python"

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -c|--command)
    COMMAND="$2"
    shift # past argument
    shift # past value
    ;;
    -i|--interpretator)
    PYTHONINTERPRETATOR="$2"
    shift # past argument
    shift # past value
    ;;    
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters


if [[ "$COMMAND" == "deploy" ]]; then
    rm -rf "$VENVSRC"
    rm -rf "$VENV"
    # if [[ ! -d "$VENV" ]]; then
    $PYTHONINTERPRETATOR -c "import sys; print 'Global sys.path is: ', '\n    '.join(sys.path)"
    git clone --depth=1 https://github.com/pypa/virtualenv.git $VENVSRC
    $PYTHONINTERPRETATOR $VENVSRC/virtualenv.py -v -p python2.7 $VENV
    # virtualenv -p python2.7 $VENV
    $VENV/bin/pip install -U pip
    $VENV/bin/pip install pyasn1 pycrypto pyOpenSSL pyparsing appdirs ctypes
    $VENV/bin/pip install cryptography service_identity psutil enum34 ipaddress cffi pkgversion
    $VENV/bin/pip install twisted
    $VENV/bin/python -c "import sys; print 'BitDust virtualenv sys.path is: ', '\n    '.join(sys.path)"
    # fi
fi


if [ "$COMMAND" == "clone" ]; then
    # if [[ ! -d "$SRC" ]]; then
    rm -rf "$SRC"
    git clone --depth=1 https://github.com/vesellov/bitdust.devel.git $SRC
    # fi
fi


if [[ "$COMMAND" == "start" ]]; then
    $VENV/bin/python $SRC/bitdust.py detach
fi


if [[ "$COMMAND" == "stop" ]]; then
    $VENV/bin/python $SRC/bitdust.py stop
fi


if [[ "$COMMAND" == "config" ]]; then
    $VENV/bin/python $SRC/bitdust.py set debug 14
fi



