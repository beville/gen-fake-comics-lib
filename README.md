# gen-fake-comics-lib
A small command-line utility that generates a slew of fake one-page comics for testing comic servers.  

Generated comics are sequenced by publisher, series, volume and issue, and all include ComicInfo.xml with basic fields populated. Some type of extra metadata can be optionally generated, such as locations, characters, credits, teams, summaries, story arcs.  Additionally, files may be created all in a single folder, or a structured subfolders based on publisher/series/volume.

The generated covers will contain the the basic details of publisher, series, volume, and issue number, as well as a fake publish date that starts with a random year for a given publisher and is incremented by one month for each issue, spanning series and volumes for that publisher.  The color for each volume of a given series will be chosen randomly.

![Sample server screenshot of generated covers](./screenshot.png)

## Requirements

    python -m pip install pillow wonderwords

## Usage

    $ ./gen-fake-comics-lib.py -h
    usage: gen-fake-comics-lib.py [-h] [-p PUB] [-s SERIES] [-v VOLUMES] [-i ISSUES] [-d DEST] [-t] [-c] [-T] [-S] [-a]

    Generate a slew of fake one page comics to test a comic server

    options:
    -h, --help            show this help message and exit
    -p PUB, --publishers PUB
                            How many publishers (default: 2)
    -s SERIES, --series SERIES
                            How many series per publisher (default: 2)
    -v VOLUMES, --volumes VOLUMES
                            How many volumes per series (default: 2)
    -i ISSUES, --issues ISSUES
                            How many issues per volume (default: 10)
    -d DEST, --dest DEST  Destination path (default: fake_comics)
    -t, --tree            Create a tree of folders, instead of dumping all in a the same folder
    -c, --credits         Populate random credits
    -T, --tags            Populate random tags
    -S, --summaries       Populate random summaries
    -a, --arcs            Populate story arcs

## Example


    $ ./gen-fake-comics-lib.py -t -p 50 -s 20 -v 2 -i 10 -d ./fakelib -tcTSa
    Going to create 20000 fake comics!
    * Destination folder: './fakelib'
    * Folder tree based on publisher/series/volume
    * Random credits will be created
    * Random tags will be created
    * Random summaries will be created
    * Story arcs will be created
    * 50 publishers
    * 20 series per publisher
    * 2 volumes per series
    * 10 issues per volume

    Continue (y/n) y
    Generating...
    Done.


