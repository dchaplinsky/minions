#!/bin/sh
set -e

version_file=${STATIC_ROOT}/.version

if [ "$#" -eq 1 ] && [ "$1" = 'gunicorn' ]; then
  command="$1 -w ${APP_WORKERS} --keep-alive 120 -t 120 --chdir ${PREFIX} --bind 0.0.0.0:8000 ${APP_NAME}"
  # copy media if not
  if ! [ -f ${version_file} ] || [ $(cat ${version_file}) != ${VERSION} ]; then
    rm -rf ${STATIC_ROOT}/*
    cp -a ${STATIC_ROOT_SOURCE}/* ${STATIC_ROOT}/
    echo -n ${VERSION} > ${version_file}
  fi
else
  command="$@"
fi

if [ "$1" = 'gunicorn' -a "$(id -u)" = '0' ]; then
	exec su-exec app $command
else
  exec $command
fi
