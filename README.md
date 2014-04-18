# UW Open Data

![UW Open Data](https://raw.github.com/karan/UW-OpenData/master/UW.png)

A comprehensive, open Python API for online services at the [University of Washington](http://washington.edu). This includes, but is not limited to the Course Catalog and Directory.

## Installation
To install this package, you have to first clone the repository using the following:
```bash
pip install -r requirements.txt
```

After doing this, you should now be able to install UW-OpenData, as shown below:
```bash
python setup.py build
```
*Note:* The [sudo] in the next step may be required (depending on your system configuration)
```bash
[sudo] python setup.py install
```

## Usage

**Output:** JSON

### `/<course code>`

Returns all courses for the requested code.

### Example:

    $ python app.py
    $ curl -i http://localhost:5000/cse

## Contribute

If you want to add any new features, or improve existing ones, feel free to send a pull request!

## Note

This project is currently in development, and is *not* ready for use.