*** Settings ***
Library    ../base/baseAction.py

*** Variables ***
${url}          https://demo.automationtesting.in/Frames.html
#${url}          https://opensource-demo.orangehrmlive.com/

*** Keywords ***

Launch Browser
    Open Browser            chrome
#    Go To Url               ${url}
