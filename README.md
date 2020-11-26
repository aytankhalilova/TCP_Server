# TCP_Server
    This is client-server-based console app “web_scraper”.
 # Scenario 
 * server-side: The server must be started and wait the request from the client. Server must produce the web scraping of the webpage to get two parameters:
the number of pictures and the number of the leaf paragraphs. The leaf paragraphs in HTML document represents only the last paragraphs in the nested paragraphstructures
 * client-side: The client must send the request to the server to get the proper answer. The client has options page (-p) to get the statistical data.
    
# Installation
 To download console app, you need to type following command:<br/>
  * git clone https://github.com/aytankhalilova/TCP_Server.git<br/>
  
 Then install requirements to have all packets needed for this project:<br/>
 * pip install requirements.txt<br/>
 
 # Usage
 For server and client, open 2 terminal tabs and run the following commands:
 * Server Terminal:<br />
      python3 web_scraper.py <br />
 
 * Client Terminal: <br />
      python3 web_scraper.py client -p [URL]
