# Flopy

This is a really old project that I had recently remembered about and wanted to archive it in a place better then OneDrive.

It takes python code and creates a "flow chart" of the code. The program can also write code using the flowchart build.

## Requirements

* Python 2.7
* IronPyton 2.7.9
  * See <https://github.com/IronLanguages/ironpython2/issues/717> to see why 2.7.10 doesn't work

## To Build

1) Ensure `C:\Program Files\IronPython 2.7` is in PATH
2) Run `.\build.ps1` from your root directory

## To Run compiled program

1) Set your working directory to `.\out`
    * The python wpf code is looking for the xaml file in the execution directory. Too lazy to fix it.
2) Run `.\flopy.exe`

See [Flopy Documentation](<Flopy Documentation.pdf>) for instructions on how to use Flopy
