# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi

alias ll='ls -la'

export GOROOT="/usr/local/go"
export GOPATH="/home/{{ ansible_user }}/.go"

export PATH="$PATH:${GOPATH}/bin:${GOROOT}/bin"

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions