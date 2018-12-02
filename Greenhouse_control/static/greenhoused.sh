#! /bin/sh

# Quick start-stop-daemon example, derived from Debian /etc/init.d/ssh
set -e

# Must be a valid filename
NAME=greenhouse
PIDFILE=/var/run/$NAME.pid
#This is the command to be run, give the full pathname
DAEMON=/greenhoused.py
DAEMON_OPTS="8888"

export PATH="${PATH:+$PATH:}/usr/sbin:/sbin"

case "$1" in
  start)
        echo -n "Starting daemon: "$NAME
        start-stop-daemon --make-pidfile --background --start --
pidfile $PIDFILE --exec $DAEMON -- $DAEMON_OPTS
        echo "."
        ;;
  stop)
        echo -n "Stopping daemon: "$NAME
        start-stop-daemon --stop --oknodo --pidfile $PIDFILE
        echo "."
        ;;
  restart)
        echo -n "Restarting daemon: "$NAME
        start-stop-daemon --stop  --oknodo --retry 30 --pidfile
$PIDFILE
        start-stop-daemon --make-pidfile --background --start --
pidfile $PIDFILE --exec $DAEMON -- $DAEMON_OPTS
        echo "."
        ;;

  *)
        echo "Usage: "$1" {start|stop|restart}"
        exit 1
esac

exit 0