# Harry J.E Day for Freelancer CTF
# Date: 7/04/16

#this is to avoid them just running exit
lsl() {
    echo "ls $@"
    ls $@ | sed s/passwordFile.txt//gi
}

findFixed() {
    find $@ | sed s/passwordFile.txt//gi
}

alias ls=lsl

alias dir=lsl

alias find=findFixed

bind -u complete

set -f