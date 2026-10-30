\# Ever After High: Community Wiki Web Scraping Project



\## Research Question



How does the Ever After High community wiki represent characters from traditional fairy tales, particularly through their story origins, Royal or Rebel identities, and connections to other characters?



\## Why I Chose This Wiki



I chose the Ever After High Miraheze wiki because I am interested in fairy tales, fairy-tale retellings, and how familiar stories are adapted into new media. Ever After High reimagines characters from traditional fairy tales as students attending a school where their family stories influence their futures.



I wanted to explore how a fan community documents these characters and connects them to their original fairy-tale backgrounds. This information could be useful to researchers studying fan communities, adaptation, popular culture, and how people preserve and organize information about fictional worlds.



\## Website Information and Policies



Wiki: https://everafterhigh.miraheze.org/



Starting page: https://everafterhigh.miraheze.org/wiki/Character\_Biographies



Robots.txt: https://everafterhigh.miraheze.org/robots.txt



Miraheze Terms of Use: https://meta.miraheze.org/wiki/Terms\_of\_Use



I selected this wiki because it is hosted on Miraheze rather than Fandom, which was excluded from this assignment.



I tested the starting page using Python's requests library and received an HTTP 200 response. I also retrieved the robots.txt file and used Python's RobotFileParser to check the starting article. The result was True, meaning that the article was not disallowed for my scraper under the general crawler rules.



The robots.txt file disallows certain administrative, API, and special-page paths. My scraper only requests ordinary wiki article pages. It identifies itself with a User-Agent header and waits five seconds between requests to reduce server load.



The robots.txt check does not automatically grant permission under every other website policy. I also reviewed the platform's Terms of Use and will stop if the wiki restricts automated access or returns an unsuccessful response.



\## Data Collection Method



I created a Python scraper using the requests and BeautifulSoup libraries.



The scraper collects two types of pages:



1\. The Character Biographies listing page.

2\. Individual character articles linked from that listing.



For each page, I collect its title, URL, page type, word count, character count, and number of unique internal links. For individual character articles, I also attempt to collect the character's fairy-tale origin and Royal or Rebel affiliation when these appear in the article infobox.



The scraper collects a maximum of 20 individual character articles and saves the results in a CSV file called `ever\_after\_high\_data.csv`.



\## Reflection: What Does the Data Measure?



The measurements in this dataset are proxies for how information is presented and organized on the wiki. Word counts and character counts describe article length, while internal-link counts show how many other wiki pages are connected to an article. These measurements do not directly reveal how popular or important a character is. For example, a character with a longer biography is not necessarily more significant to the Ever After High story or its fans. The number of links can also depend on how editors organize information and how many related articles exist. Since I am only examining a small sample of articles linked from one biography listing, my results cannot represent the entire wiki or all fan opinions about the franchise.



\## Results



\## Results



The scraper successfully collected data from 19 pages: the Character Biographies listing page and 18 individual character articles. The characters included Apple White, Raven Queen, Briar Beauty, Madeline Hatter, Ashlynn Ella, Hunter Huntsman, Cerise Hood, Cedar Wood, C.A. Cupid, Blondie Lockes, Dexter Charming, Poppy O'Hair, Holly O'Hair, Rosabella Beauty, Darling Charming, Melody Piper, Meeshell Mermaid, and Farrah Goodfairy.



The collected data allows comparisons between character biographies based on their word counts, character counts, and internal-link counts. It also attempts to record each character's fairy-tale origin and Royal or Rebel affiliation when that information is available in the article. Overall, the dataset provides a small sample of how the Ever After High wiki organizes its characters and connects them to traditional fairy tales and other characters.

\## Project Files



\- `wiki\_scraping.py` — Python web scraper.

\- `ever\_after\_high\_data.csv` — Collected wiki data.

\- `README.md` — Research question, website policies, methods, and reflection.

\- `first\_web\_scraper.py` — Original course practice scraper.

