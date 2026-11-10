\# GETting Culture Across APIs



\## Project Overview



For this assignment, I chose to compare the MediaWiki Action API and the Open Library API. I chose Open Library because I am interested in books and fairy-tale retellings, and I wanted to explore how different APIs organize information about literature.



\## API 1: MediaWiki Action API



\- \*\*Website:\*\* https://www.wikipedia.org/

\- \*\*Endpoint:\*\* https://en.wikipedia.org/w/api.php

\- \*\*Information retrieved:\*\* The Rapunzel Wikipedia article, including its title, URL, and introductory extract.

\- \*\*Authentication:\*\* No API key or account required.

\- \*\*Data format:\*\* JSON.



The API returned information explaining the origins of the Rapunzel fairy tale, including its publication by the Brothers Grimm in 1812 and earlier versions of the story.



\## API 2: Open Library API



\- \*\*Website:\*\* https://openlibrary.org/

\- \*\*Endpoint:\*\* https://openlibrary.org/search.json

\- \*\*Information retrieved:\*\* Five books titled Rapunzel, including their titles, authors, publication years, edition counts, and Open Library identifiers.

\- \*\*Authentication:\*\* No API key or account required for the search used in this project.

\- \*\*Data format:\*\* JSON.



The five results included books by Paul O. Zelinsky (1997), Shannon Hale and Nathan Hale (2008), the Brothers Grimm (1960), Barbara Rogasky (1982), and Bethan Woollvin (2017).



\## Connecting the APIs



I connected the two APIs by taking the first book returned by Open Library, \*Rapunzel\* by Paul O. Zelinsky (1997), and searching for its title using the MediaWiki Action API.



The Wikipedia search returned five possible results: "Rapunzel," "Rapunzel (Tangled)," "Tangled," "Flynn Rider," and "Rapunzel (disambiguation)." However, these results did not establish that Wikipedia had a dedicated article about Paul O. Zelinsky's specific book.



This was an interesting finding because both APIs contained information about Rapunzel, but they organized the information differently. Open Library distinguished between individual books and their editions, while Wikipedia focused more on the fairy tale and its broader cultural influence. The search also demonstrated that matching records across APIs can be difficult when different cultural works share the same title.



\## Comparing the APIs



Both APIs provide access to cultural information, but they organize that information differently. The MediaWiki Action API provides encyclopedia information, including article extracts and page information, while Open Library provides bibliographic information about books, including authors, publication years, and editions. Both APIs return structured JSON, which makes them relatively easy to work with using Python's requests library. Neither required an API key or an account for this project, although both benefit from descriptive User-Agent headers.



Their rate limits also reflect different expectations about usage. Wikimedia allows up to 200 requests per minute for requests with a compliant User-Agent, while unidentified requests are limited to 10 per minute. Open Library allows one request per second by default and up to three requests per second for identified applications that provide a User-Agent and contact information. These restrictions encourage responsible API use and help prevent automated requests from overwhelming the services.



The two services also have different organizational backgrounds. Wikipedia is supported by the nonprofit Wikimedia Foundation, while Open Library is a project of the nonprofit Internet Archive. Open Library describes its mission as creating a catalog of books, with contributions from libraries and individual users.



There are also limitations to what these APIs represent. Wikipedia focuses on subjects that have received enough attention to warrant encyclopedia articles, while Open Library focuses on catalogued books and their bibliographic information. This means that lesser-known fairy tales, oral storytelling traditions, and books with limited distribution may be less visible in these datasets. Even when both APIs return information about the same subject, they do not necessarily provide the same perspective on it.



This comparison demonstrates that APIs are not neutral collections of cultural information. Their organizational purposes, cataloguing practices, and data structures influence what researchers can find and what remains difficult to discover. As a researcher using APIs designed primarily for developers, I also noticed that finding a relevant cultural connection requires interpretation rather than simply matching titles.



\## Files



\- `getting\_culture.py` — Python script that queries both APIs and connects their results.

\- `rapunzel\_open\_library\_data.json` — Selected data retrieved from the APIs.



\## Sources



\- \[MediaWiki API Etiquette](https://www.mediawiki.org/wiki/API:Etiquette)

\- \[Wikimedia API Rate Limits](https://www.mediawiki.org/wiki/Wikimedia\_APIs/Rate\_limits)

\- \[Open Library API Documentation](https://openlibrary.org/developers/api)

\- \[About Open Library](https://openlibrary.org/about)

