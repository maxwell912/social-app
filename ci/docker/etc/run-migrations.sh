#!/bin/bash
echo -e '\033[0;34m--- run migrations ---\033[0m'
/etc/rattus.sh
python3 manage.py migrate