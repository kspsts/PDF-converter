# PDF Web App

PDF Web App is a Flask-based web application for processing PDF documents. This application allows users to upload PDF files, process them, and potentially convert them into text or DOCX format.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To run this project, you will need:

- Docker
- Python 3
- Packages from `requirements.txt`

### Installation

1. Clone the repository:

```git clone [repository-url]```

2. Navigate to the project directory:

```cd pdf-web-app```

3. Build and run the Docker container:
```
docker build -t pdf-web-app .
docker run -p 80:5000 pdf-web-app
```


## Usage

Describe how to use your application after launching: how to upload files, what features are available, etc.

## Technologies

- [Flask](http://flask.pocoo.org/) - The web framework used in the project
- [Pytesseract](https://pypi.org/project/pytesseract/) - OCR library used in the project
- [Docker](https://www.docker.com/) - Used for containerizing the application
