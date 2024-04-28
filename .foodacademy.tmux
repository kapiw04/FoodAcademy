#!/bin/zsh

SESSIONNAME="FoodAcademy"
tmux has-session -t $SESSIONNAME &> /dev/null

if [ $? != 0 ]
then
    tmux new-session -s $SESSIONNAME -n script -d
    tmux split-window -h -t $SESSIONNAME
    tmux send-keys -t $SESSIONNAME:0.0 'cd ~/FoodAcademy && source backend/.venv/bin/activate && clear' C-m
    tmux send-keys -t $SESSIONNAME:0.1 'cd ~/FoodAcademy && source backend/.venv/bin/activate && clear' C-m
fi

tmux attach -t $SESSIONNAME

