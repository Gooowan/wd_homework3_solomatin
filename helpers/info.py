endpoints_info = {
  "endpoints": [
    {
      "path": "/",
      "method": "GET",
      "description": "Get endpoints information",
    },
    {
      "path": "/text",
      "method": "GET",
      "description": "Get pure text",
    },
    {
      "path": "/books",
      "method": "GET",
      "description": "Get a list of books in JSON format",
    },
    {
      "path": "/movies",
      "method": "GET",
      "description": "Get a list of movies in JSON format",
    },
    {
      "path": "/html",
      "method": "GET",
      "description": "Get static HTML file",
    },
    {
      "path": "/image",
      "method": "GET",
      "description": "Get image",
    },
    {
      "path": "/books?",
      "method": "GET",
      "description": "Get details of a specific book",
      "query_parameters": "Specify in the query parameters bookId",
    },
    {
      "path": "/",
      "method": "POST",
      "description": "Receive a POST request ad simple response json",
    },
    {
      "path": "/add",
      "method": "POST",
      "description": "Add data via POST request and receive an updated list. attach json in body of request",
    }
  ]
}
