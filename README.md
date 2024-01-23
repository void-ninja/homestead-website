# homestead-website
A website that I host on a machine on my local network that is used for various homestead related things.

A lot of the main setup for the backend was based on flasks official tutorial https://flask.palletsprojects.com/en/3.0.x/tutorial

to start:
from homestead-website directory, run 
`source .venv/bin/activate`
to activate the virtual environment, then run
`gunicorn -b 0.0.0.0:80 -w 4 homestead_app:app`
to start the server, listening on port 80, which is the default browser port,
with 4 workers

supervisor has it running on startup ^

to access the server, navigate to HOSTNAME/ in a web browser, where HOSTNAME is the 
hostname of the device you are hosting the server on. The / tricks the browser into 
treating the hostname as a url instead of a web search, but http://HOSTNAME would also 
work if the slash doesnt