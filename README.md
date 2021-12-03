# ECM1400CourseWork

This is the covid 19 dashboard for ECM1400. It is 100% of the assessment and needs to follow the [spec](https://github.com/r-3than/ECM1400CourseWork/blob/13ffd0a71cb45845f973258022094663d4f85d0d/CA-specification.pdf) provided.

## Features or examples

Here is what the dashboard looks like:
![Dash board photo](https://github.com/r-3than/ECM1400CourseWork/blob/3c38741270c0561ecaa0d0468866896806a4aa02/exampleDashboard.png)

## Requirement(s)

These are the requirements:
+ [python 3.9 +](www.python.org/downloads/release/python-399)
+ [uk-covid19](https://github.com/publichealthengland/coronavirus-dashboard-api-python-sdk)
+ [newsapi](https://newsapi.org/docs/client-libraries/python)

## Installation / Getting Started

First get an api from [here](https://newsapi.org/register)
Then put this apikey into apikey.txt.

Then install python3.9 +
You can either install the modules or use the virtual environments to run the project:

Without venvs:
    pip3 install uk-covid19
    pip3 install newsapi-python
    python3 main.py
    Go to localhost:5000/index

With venvs:
    Make sure python 3.9 + is installed
## Usage

With venv(linux - Ubuntu(debian)):
    ./start.sh
    Go to localhost:5000/index

With venv(Windows - powershell):
    .\WindowsVenv\Scripts\Activate.ps1
    python main.py
    Go to localhost:5000/index

With venv(Windows - cmd):
    .\WindowsVenv\Scripts\activate.bat
    python main.py
    Go to localhost:5000/index
## Contributors

Ethan Ray (r-3than)

## License

MIT LICENSE

Copyright (c) <2021> <Ethan Ray>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

