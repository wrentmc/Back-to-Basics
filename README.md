# Back to Basics
## A programming language written entirely in Python
This language, as referenced by its name, simulates programming in the early days of coding[^1]. It is compiled **and** interpreted!

## How to use
1) Head to the release page of this Repo and download the current release.
2) Write a BTB script (examples [here](https://github.com/wrentmc/Back-to-Basics/tree/main/examples)) using available commands (run `btb.exe -h` for help)
3) Run `btb.exe <your file>`

## Flags
Currently, BTB supports the following flags:
|Flag|Alias|Description|
|:---:|:---|---|
|-h|(--help)|show this message|
|-c|(--commands)|show command list|
|-n|(--notitle)|do not show title|
|-C|(--compile)|compile your source file into an executable. Change icon.ico to change the compiled icon.|

## Compilation
Let's call our file `source.btb` for this example and assume it works.<br>
We would run `btb.exe source.btb -C` and accept the notice.<br>
NOTE: An existing `out.exe` will be overwritten!<br>
After waiting for a little, we'll have our `out.exe` in the same directory that we ran the command in. This file can now be distributed!<br>
NOTE: If icon.ico is not present, one will be created.

[^1]: Obviously, it is much simpler than, say, assembly or COBOL.
