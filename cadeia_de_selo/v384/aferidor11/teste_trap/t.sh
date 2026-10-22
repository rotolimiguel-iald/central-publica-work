#!/bin/sh
T="$1"
echo $$ > "$T/x.pid"
trap 'rm -f "$T/x.pid"; echo EXIT_TRAP_RODOU >> "$T/saida.txt"' EXIT
sleep 30 &
wait $!
