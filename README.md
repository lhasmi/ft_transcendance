# ft_transcendance
# see the notion page for detailled logs

### testing the Apis with curl
# To test the Player list and creation endpoint:


# To get a list of players
curl -X GET http://localhost:8000/players/ -H 'Accept: application/json'

# To create a new player
curl -X POST http://localhost:8000/players/ \
     -H 'Content-Type: application/json' \
     -d '{"username": "newplayer", "email": "player@example.com"}'

# Replace localhost:8000 with your actual server’s URL if not testing locally.

#### Testing with Postman

#    Get Request:
        First,download and install Postman from Postman's official site.
Setting Up a GET Request in Postman

 to set up a GET request:

    Create a New Request
        Click on the "New" button or the "+" tab to create a new request tab.

    Set the HTTP Method to GET
        To the left of the URL field, there is a dropdown menu that likely says "GET" by default. If it is set to another method (like POST), click the dropdown and change it to GET.

    Enter the Request URL
        In the URL field, enter the full URL of the API endpoint you wish to test. For example: http://localhost:8000/players/
        Enter the URL http://localhost:8000/players/.
        Hit send and see the JSON response.

#    Post Request:
        Set the method to POST.
        Enter the URL http://localhost:8000/players/.
        Under Headers, set Content-Type to application/json.
        In the body, select raw and input a JSON object: {"username": "newplayer", "email": "player@example.com"}.
        Hit send to create a new entry.