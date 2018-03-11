#!/usr/bin/env bash

case $1 in
list)
   curl http://0.0.0.0:5000/
   ;;
describe)
   curl http://0.0.0.0:5000/$2/description
   ;;
help)
    echo <<EOF
Usage:
   voodoo list -- list available services
   voodoo describe $service -- get information about $service
   voodoo $service -- use service
EOF
   ;;
*)
   curl -F 'data=@-' http://0.0.0.0:5000/$1
   ;;
esac
