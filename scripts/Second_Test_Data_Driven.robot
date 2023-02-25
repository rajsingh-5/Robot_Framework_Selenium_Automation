*** Settings ***
Library                 ../base/baseAction.py
Resource                 ../pageObjects/Resource.robot
Library                 DataDriver          ../Data/data.xlsx
Test Setup               Launch Browser
Test Teardown            Close Browser
Test Template           TC1
*** Test Cases ***
TC1
    TC1

*** Keywords ***
TC1
    [Arguments]                 ${urlData}
    Go To Url                   ${urlData}
#    Go To Url                   https://demo.automationtesting.in/Frames.html
#    Click                       xpath|//a[@href="#Multiple"]
#    Handle Frame                1           0
#    Send Keys                   xpath|//*[@type="text"]             asdfg
#    Sleep                       3
#    Handle Frame                default
#    Click                       xpath|//*[text()="Home"]
#
TC2
    Go TO Url                   https://practice.automationtesting.in/
    Scroll Down                 full
    Sleep                       3
    Scroll Up                   full
    Sleep                       3

#TC3
#
#    Go To Url                   https://demo.automationtesting.in/Register.html
#    Click                       xpath|//*[text()="Widgets"]             hover=True
#    Sleep                       3
#    Click                       xpath|//a[contains(.,'Accordion')]
#    Verify                      xpath|//b[text()="Collapsible Group 1 - Readability"]           Collapsible Group 1 - Readability
#
#TC4
#    Go To Url                   https://practice.automationtesting.in/
#    Scroll To Element           xpath|//h4[@class="widgettitle"]
#    Sleep                       3
