*** Settings ***
Resource  resource.robot

*** Test Cases ***
Changed Read Status Shows In List
    Create Three Tips
    Change Tip Read Status  1
    Change Read Filter Setting
    Change Read Filter Setting
    Input 2 Command
    Input x Command
    Run Application
    Output Should Contain  id:1 newTip1, www.test.test