# klipper control python
    This Python project is written by Euris Montanez.

        This is my first project that I plan to complete, so I would appreciate any help that can point me 
    in the right direction. Thanks!

# Usage:
    python server.py "klipperip"

# About
        In this python project my aim is to be able to make a website that allows me to see and control my 
    3d printer. At minimum I would like to be able to see a constant temperature update of all of my tools 
    (ie: Extruder, Hot Bed, and etc) temperatures. The most important thing is to have a webcam that is able
    to detect when something in the print goes wrong (ie: stringing, warping, and etc).


# TODO Learning:
        In order to finish my code I need to learn how to first code a webhook, then be able to use that 
    webhook on my website. The most important thing right now to focus on is getting my current code to be,
    able to interact with flask, http, and webhooks.


# TODO Moonraker API:
        The Moonraker API, is really easy to understand. The things I want to implemnt in my code would be the 
    endpoint that retrieves a webcams stream.


# TODO HTML:
        I am familiar with HTML, so hopefully getting back into it is easy. My main objective with HTML
    is to beable to create a website that is visually appealling and functional. I believe that the best way 
    to make this 'GUI' work is to use webhooks, which allows the server to automatically update a variable from a server.


# TODO Webcamera:
        I need to be able to see my printer while on the website. I would also like to use an ai that checks 
    for failed prints, like the pasta detector we all know and love.


# Learned
        So far I have learned how to interact with dictionaries and arrays through APIs with the 
    request package. I also learned how to structure my code in a way that makes it possible
    for the main function to call every single function. I understand websockets, I don't need to make my own
    since the moonraker api brings it's own webhooks.