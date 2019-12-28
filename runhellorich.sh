#!/bin/sh

### BEGIN INIT INFO
# Provides:           runhellorich.sh
# Required-Start:     $remote_fs $syslog
# Required-Stop:      $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:       0 1 6
# Short-Description:  Start daemon at boot time
# Description:        Says Hello Rich!
### END INIT INFO

DIR=/home/pi/PythonCode
DAEMON=$DIR/hellorich.py
DAEMON_NAME=hellorich

DAEMON_OPTS=""

DAEMON_USER=pi

PIDFILE=/var/run/$DAEMON_NAME.pid

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "starting system $DAEMON_NAME daemon"
    start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --startas $DAEMON -- $DAEMON_OPTS
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "stopping system $DAEMON_NAME daemon"
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc "$DAEMON_NAME" "DAEMON" && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}:"
    exit 1
    ;;

esac
exit 0
