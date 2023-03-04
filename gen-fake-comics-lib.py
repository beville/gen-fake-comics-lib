#!/usr/bin/env python3

import sys
import os
import random
import colorsys
import hashlib
import zipfile
import time
import math
from pathlib import Path
from argparse import ArgumentParser
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from wonderwords import RandomSentence

#-------------------------------------------
def parseArgs():

    default_publishers = 2
    default_series = 2
    default_volumes = 2
    default_issues = 10
    default_dest = "fake_comics"
    
    parser = ArgumentParser()
    parser.description = "Generate a slew of fake one-page comics to test a comic server"

    parser.add_argument("-p", "--publishers", dest="publishers",
                        default=default_publishers,
                        type=int,
                        help=f"How many publishers (default: {default_publishers})",
                        metavar='PUB')   

    parser.add_argument("-s", "--series", dest="series",
                        default=default_series,
                        type=int,
                        help=f"How many series per publisher (default: {default_publishers})",
                        metavar='SERIES')                         

    parser.add_argument("-v", "--volumes", dest="volumes",
                        default=default_volumes,
                        type=int,
                        help=f"How many volumes per series (default: {default_volumes})",
                        metavar='VOLUMES') 

    parser.add_argument("-i", "--issues", dest="issues",
                        default=default_issues,
                        type=int,
                        help=f"How many issues per volume (default: {default_issues})",
                        metavar='ISSUES') 

    parser.add_argument("-d", "--dest", dest="dest",
                        default=default_dest,
                        help=f"Destination path (default: {default_dest})",
                        metavar='DEST') 

    parser.add_argument("-t", "--tree", dest="tree",
                        action="store_true", default=False,
                        help=f"Create a tree of folders, instead of dumping all in a the same folder")    

    parser.add_argument("-c", "--credits", dest="credits",
                        action="store_true", default=False,
                        help=f"Populate random credits")                                                                         

    parser.add_argument("-T", "--tags", dest="tags",
                        action="store_true", default=False,
                        help=f"Populate random tags")    

    parser.add_argument("-S", "--summaries", dest="summaries",
                        action="store_true", default=False,
                        help=f"Populate random summaries")    

    parser.add_argument("-a", "--arcs", dest="arcs",
                        action="store_true", default=False,
                        help=f"Populate story arcs")    

    args = parser.parse_args()                
    
    error = False

    # TODO add some validation here

    if error:
        sys.exit(-1)      

    return args

#------------------------------------------
def genXml(series,volume,publisher,issue, year, month, cover_size, cover_w, cover_h, 
            add_tags=False, add_credits=False, add_storyarc=False, add_summary=False):

    tags = ""
    credits = ""
    story_arc = ""
    summary_text = "This a test comic!"

    if add_summary:
        summary_text = ""
        # create a random 10 sentence summary
        s = RandomSentence()
        for i in range(10):
            summary_text += s.sentence() + " "

    summary = f"<Summary>{summary_text}</Summary>"

    if add_storyarc:
        # make a new arc every five issues
        arc_num = math.floor((issue-1)/5) + 1
        story_arc = f"<StoryArc>Story {series}-{volume}-{arc_num}</StoryArc>"

    if add_tags:
        possible_teams = 2000
        possible_locations = 2000
        possible_characters = 15000

        locations_count = random.randint(1, 10)
        teams_count = random.randint(1, 5)
        characters_count = random.randint(1, 20)
        
        tags = tags + "<Locations>"
        for l in range(locations_count):
            location = random.randint(1, possible_locations)
            tags = tags + f"Location{location:05},"
        tags = tags[:-1] + "</Locations>\n"
        
        tags = tags + "<Teams>"        
        for t in range(teams_count):
            team = random.randint(1, possible_teams)
            tags = tags + f"Team{team:05},"
        tags = tags[:-1] + "</Teams>\n"

        tags = tags + "<Characters>"        
        for t in range(characters_count):
            character = random.randint(1, possible_characters)
            tags = tags + f"Character{character:05},"
        tags = tags[:-1] + "</Characters>\n"

    if add_credits:
        possible_people = 5000
        
        credit_types = ["Writer", "Penciller", "Inker", "Colorist", "Letterer", "CoverArtist", "Editor"]

        for credit in credit_types:
            credits = credits + f"<{credit}>"
            for p in range(random.randint(1, 3)):
                person = random.randint(1, possible_people)
                credits = credits + f"Person{person:05},"
            credits = credits[:-1] + f"</{credit}>\n"

    xml =   f"""<?xml version=\'1.0\' encoding=\'utf-8\'?>
<ComicInfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <Title>Title of {series} v{volume} #{issue}</Title>
    <Series>{series}</Series>
    <Number>{issue}</Number>
    <Volume>{volume}</Volume>
    {story_arc}
    {summary}
    <Notes>Auto-generated test comic</Notes>
    <Web>https://github.com/beville/gen-fake-comics-lib</Web>
    <Year>{year}</Year>
    <Month>{month}</Month>
    <Day>1</Day>
    <Publisher>{publisher}</Publisher>
    <PageCount>1</PageCount>
    {tags}
    {credits}
    <Pages>
        <Page Image="0" ImageHeight="{cover_h}" ImageSize="{cover_size}" ImageWidth="{cover_w}" Type="FrontCover" />
    </Pages>
</ComicInfo>"""

    return xml
#------------------------------------------
def genCoverImage(series,volume,publisher,issue, month, year, height=800):
    
    width = int(height * 663 / 1024)

    # Make color be based on hash of series+volume+publisher
    # so all issues of a given series are the same
    seed_base = series+volume+publisher
    color_seed = hashlib.md5(seed_base.encode('utf-8')).digest()
    random.seed(color_seed)

    # Pick a random color, that is a bit bright
    h,s,l = random.random(), 0.5 + random.random()/2.0, 0.4 + random.random()/5.0
    r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]

    # re-seed the random lib for subsequent calls
    random.seed(time.time())

    image = Image.new(mode = "RGB", size = (width,height), color = (r,g,b))

    lines = []
    lines.append(f"{series}")
    lines.append(f"Volume {volume}")
    lines.append(f"Issue #{issue:03}")
    lines.append(f"({publisher})")
    lines.append(f"[{year}-{month:02}]")
    
    fnt = ImageFont.truetype('arial.ttf', 60)
    draw = ImageDraw.Draw(image)

    y_pos = 20
    for line in lines:
        draw.text((20,y_pos), line, font=fnt, fill="black")
        _,_,_,line_height = fnt.getbbox(line)
        y_pos = y_pos + int(line_height*1.2)
   
    return image

#-------------------------------------------
def mkdir(path):
    try:
        os.mkdir(path)
    except:
        pass
#-------------------------------------------
def main():

    args = parseArgs()

    total = args.publishers * args.series * args.volumes * args.issues
    print(f"Going to create {total} fake comics!")
    print(f" * Destination folder: '{args.dest}'")
    if args.tree:
        print(f" * Folder tree based on publisher/series/volume")
    else:
        print(f" * All files in same flat folder")
    if args.credits:
        print(f" * Random credits will be created")        
    if args.tags:
        print(f" * Random tags will be created")        
    if args.summaries:
        print(f" * Random summaries will be created")        
    if args.arcs:
        print(f" * Story arcs will be created")        

    print(f" * {args.publishers} publishers")
    print(f" * {args.series} series per publisher")
    print(f" * {args.volumes} volumes per series")
    print(f" * {args.issues} issues per volume")
    print()
    answer = input("Continue (y/n) ") 
    if answer.lower() not in ["yes", "y"]: 
        print("Okay, quitting.")
        sys.exit(-1)
    
    print("Generating...")

    mkdir(args.dest)
    dest_path = Path(args.dest)
    
    for p in range(1,args.publishers+1):
        # pick a random start year for each publisher
        year = random.randint(1938, 2000)
        month = 0
        publisher = f"Publisher{p:03}"
        if args.tree:
            pub_dir = Path(args.dest) / publisher
            mkdir(pub_dir)

        for s in range(1,args.series+1):
            series = f"Series P{p:03}S{s:03}"
            if args.tree:
                series_dir = pub_dir / series
                mkdir(series_dir)            
            for v in range(1,args.volumes+1):
                if args.tree:
                    volume_dir = series_dir / Path(series + f" v{v}")
                    mkdir(volume_dir)  

                    # Set the "tree-mode" dest dir for the fake comic
                    dest_path = volume_dir
                for i in range(1,args.issues+1):
                    volume = str(v) 
                    month = month + 1
                    if month > 12:
                        month = 1
                        year = year + 1
                    issue = i
                    volume = str(v)
                    cover = genCoverImage(series, volume, publisher, issue, month, year)
                    cbzFileName = f"{series} (v{volume}) #{issue:03} ({year}).cbz"
                    outpath = dest_path / cbzFileName

                    image_buf = BytesIO()
                    cover.save(image_buf, format='JPEG')
                    cover_size = len(image_buf.getbuffer())
                    
                    xml = genXml(series,volume,publisher,issue, year, month, cover_size, 
                                cover.width, cover.height, 
                                add_tags=args.tags, add_credits=args.credits, 
                                add_storyarc=args.arcs, add_summary=args.summaries)

                    with zipfile.ZipFile(outpath, 'w') as zipped_f:
                        zipped_f.writestr("ComicInfo.xml", xml)
                        zipped_f.writestr("page01.jpg", image_buf.getbuffer())

    print("Done.")

#-------------------------------------------
if __name__ == '__main__':
    main()
