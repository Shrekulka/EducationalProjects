savedcmd_/home/shrekulka/develop/kernel/proc/proc-1/procfs-1.mod := printf '%s\n'   procfs-1.o | awk '!x[$$0]++ { print("/home/shrekulka/develop/kernel/proc/proc-1/"$$0) }' > /home/shrekulka/develop/kernel/proc/proc-1/procfs-1.mod
