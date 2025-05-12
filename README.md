## Project of SUSTech CS307: Principles of Database Systems, Spring 2024
CommuteTrack-DB is a database project designed specifically for managing commute data in the Shenzhen metro system. Key features of the project include:

* Recording detailed passenger commute information such as entry time, exit time, locations, and transaction amounts.
* Utilizing ORM (Object-Relational Mapping) to simplify complex database operations.
* Offering a frontend interface for easy data viewing and management.
* Using asynchronous programming to handle high concurrency requests.

**Contributor**: [zrhlsmt](https://github.com/zrhlsmt)
### Quick Start
Backend: run  `python Server/main.py`

Frontend: run  `python GUI/Main.py`

### Code Explanation
* `API`: To provide basic functionality of accessing a database system, these code build a back end library which exposes a set of APIs.

* `Scripts`: Process the original data recourse to generate  `.sql` `.json` `.csv` files in `Python`. Run the `.sql` or `.csv` files to import data into database.

* `Scripts_in_Java`: Same as above but written in `Java`. 

* `out` & `out_from_Java`: Contain all the files that `Scripts` generated in `python` or `Java` respectively.

* `recourse`: Contain all the recourse code that the course provided.
