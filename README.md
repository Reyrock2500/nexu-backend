# Nexu-backend exercise

This project is an implementation of a small backend service designed to be used with an already existing frontend. Its purpose is retrieving data from a JSON file and satisfy frontend's requests.

## How to build

1.  **Docker**: Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop).
2.  **WSL 2** (Windows users only): It is highly recommended to enable WSL 2 backend for Docker on Windows. [Install WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install).
3.  **Git** Make sure git is installed. [Git](https://git-scm.com/install/).
4. Clone this repo into your machine using git clone https://github.com/Reyrock2500/nexu-backend.git
5. Open a terminal in the project root directory and run:

**Building the image**
- docker build -t nexu-api .

**Running the project (if port 8000 is okay)**

- docker run -p 8000:8000 nexu-api

The API will be available at [http://localhost:8000](http://localhost:8000) and the documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## Testing
<img width="1885" height="889" alt="image" src="https://github.com/user-attachments/assets/35b7756b-765b-4ade-8ae1-0a346b383ff8" />

If you have the frontend code on hand, you can test it directly from there. If not, it's your lucky day, by going to /docs, you can interact directly with every endpoint available. There, you can test sending POST/PUT/GET, receiving a response and seeing that whatever you do, is saved in the temporary SQLite DB.
[http://localhost:8000/docs](http://localhost:8000/docs)


## Technologies used

- **Python 3.12**: Main programming language. Python's syntax is very straightforward, it also comes with good enough performance, which suits such a straightforward project.
- **FastAPI**: It is defined as a high-performance web framework for building APIs. It is also very simple to use, includes default testing/docs and is more than enought for this project's purpose.
- **SQLite**: Lightweight disk-based database for data persistence. SQL was used because that language and structure makes it very easy to manipulate and organize the provided data, as opposed to just working with the JSON file.
- **Docker**: Containerization platform, it allows anyone with it to build and run container images. For this project, it reduces the amount of actions needed by any user to run it (in this case, evaluators).
- **Pydantic**: Data validation and settings management. Mainly used for POST/PUT, makes it so the user has to comply with the desired structure of the inputs.
- **Pytest**: This is a framework for unit and integration tests.


## My experience

The logic of this entire project was really fun to work with. Not difficult at all. What I tend to struggle with is the syntax/rules of the language/libraries, nothing a quick google search can't fix. I spent a little more time than expected, as I was learning a lot about Docker and how powerful it really is. Wasted some time trying to build with misconfigurations, but in the end it all ran smoothly. Linting experience was not so pleasant. I'm looking forward to improving the code I can produce.

## What I would do with more time
As I mentioned before, the requirements are pretty straightforward, so some considerations, while they would be good for production, come as overkill for this task. With more time, maybe for experimenting, I would have implemented an independent DBMS, like Postgres or MySQL, as well as implementing heavier error-handling and maybe controlling edge-cases where there are problems with the provided data. It would also be fun, but sort of out of scope for this exercise.

## Deployment
