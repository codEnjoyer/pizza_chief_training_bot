@echo off

call %~dp0../../../venvs/pizza_chief_training_bot/Scripts/activate

cd %~dp0

set TOKEN=6145105976:AAEeYaetkZB1EEJ9ks7sWkXm42MiDZJsovU

python bot_main.py

pause
