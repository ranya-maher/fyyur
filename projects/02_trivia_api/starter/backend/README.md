# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM that we use to handle the postgres database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension that we use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
createdb trivia
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Reference

### End Points

The app currently contains the following endpoints:

```
GET '/categories'
GET '/questions'
DELETE '/questions/<int:question_id>'
POST '/questions'
POST '/search'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

```

#### GET '/categories'
* Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
* Request Arguments: None
* Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs as well as success status. 

<strong>Example: curl http://127.0.0.1:5000/categories </strong>
```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

####  GET '/questions'

* Fetches a list of all the questions under all categories paginated (10 per page), `?page=<num>` URL parameter is added to move through pages
* Request Arguments: None
* Returns: all categories, a list of question objects, success status, and total number of questions in the database.

<strong>Example: curl http://127.0.0.1:5000/questions?page=2 </strong>

```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": null,
      "category": null,
      "difficulty": null,
      "id": 25,
      "question": null
    }
  ],
  "success": true,
  "total_questions": 70
}
```

####  DELETE '/questions/<question_id>'

- Deletes a question by a given id
- Request Arguments: question_id
- Returns: Success status and id of deleted question if successful

<strong>Example: curl -X DELETE http://127.0.0.1:5000/questions/14 </strong>

```bash
{
  "deleted": 14,
  "success": true
}
```

####  POST '/questions'

* Creates a new question
* Request Arguments: An object with all attributes of a question (question, answer, category, difficulty)
* Returns: A list of all categories, ID of the newly created question, a list of questions, success status, and the total number of questions

<strong>Example: curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question": "How many legs does a cat has?", "answer": "4", "category": "1", "difficulty": 1}' </strong>

```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "created": 79,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 71
}
```

#### POST '/search'

* Fetches a list of all the questions that contains a specific search term in the "question"
* Request Arguments: searchTerm
* Returns: current category id, a list of question objects, success status, and total number of matching questions

<strong>Example: curl -X POST http://127.0.0.1:5000/search -H "Content-Type: application/json" -d '{"searchTerm": "Tom"}' </strong>

```bash
{
  "current_category": 1,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

####  GET '/categories/<category_id>/questions'

* Fetches a list of all the questions under a given category
* Request Arguments: category_id
* Returns: current category id, a list of question objects, success status, and total number of matching questions

<strong>Example: curl http://127.0.0.1:5000/categories/4/questions </strong>

```bash
{
  "current_category": 4,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

####  POST '/quizzes'

* Fetches a random question of that wasn't answered before and belonds to the same selected category
* Request Arguments: a list of previous question ids and a category object
* Returns: A question object that is not in the previous questions list and success attribute

<strong> Example: curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{previous_questions:[5, 23], quiz_category:{type: "History", id: 4}}' </strong>

```bash
{
  "question": {
    "answer": "Muhammad Ali", 
    "category": "4", 
    "difficulty": 4, 
    "id": 9, 
    "question": "What boxer's original name is Cassius Clay?"
  }, 
  "success": true
}
``` 

### Error Handling

This porject supports 4 types of errors:
* 400 - Bad Request
* 404 - Not Found
* 422 - Unprocessable
* 500 - Internal Server Error

and the response is in JSON in the following format:
```
{
    'success': False,
    'error': 400
    'message': 'bad request'
}
```


### Testing
To run the tests, run
```
dropdb trivia
createdb trivia
psql trivia < trivia.psql
python test_flaskr.py
```