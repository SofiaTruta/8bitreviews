# 8bit Reviews - description

This project was part of General Assembly’s Software Engineering Immersive Bootcamp. It aimed to familiarize me with using Python (Django) for the backend and JavaScript (React) for the frontend, while also incorporating a PostgreSQL relational database.

I am a lover of video games so I thought that a video game review website would be the perfect opportunity to develop my skills with relational databases. 

![screenshot](https://i.imgur.com/iCFR299m.png)
![screenshot](https://i.imgur.com/Dz4mBT9m.png)
![screenshot](https://i.imgur.com/GKvpEWWm.png)


## Deployment Link

https://8bitreviews-frontend-production.up.railway.app/

## Timeframe 

Solo project completed within a 7-day timeframe.

## Technologies Used

### Backend
- Python
- Django
- Django-rest-framework
- PostgreSQL

### Frontend
- JavaScript
- React
- React Bootstrap
- Node.js

Tools:
- Trello for project management
- LucidChart for ERD
- Git for version control


## Getting Started / Code installation

This project is divided into two repositories - backend and frontend. This was done for ease of deployment using Railway. 

*this is the backend repo only - please find the frontend repo [here](https://github.com/SofiaTruta/8bitreviews-frontend)*

To run this project locally, clone both repositories and start both simultaneously in your terminal. Frontend dependencies are listed in the package.json file.

Additional setup:
- a local database with postgreSQL (if you are using Mac, this is a built in app, to create a new database all you have to do is open a terminal and run the command “createdb <name>”)
- Include a .env file in both backend and frontend projects for secure data storage (refer to .env.example)
- Obtain an API key and host from RapidAPI, specifically [OpenCritic’s API](https://rapidapi.com/opencritic-opencritic-default/api/opencritic-api) for game information retrieval (there is a free version that will be enough for testing)


## MVP requirements
- Be a full-stack Django/React application.
- Connect to and perform data operations on a PostgreSQL database (the default SQLLite3 database is not acceptable).
- If consuming a third party API (OPTIONAL), have at least one data entity (Model) in addition to the built-in User model. The related entity can be either a one-to-many (1:M) or a many-to-many (M:M) relationship.  
- If not consuming an API, have at least two data entities(Models) in addition to the built-in User model. It is preferable to have at least one one-to-many (1:M) and one many-to-many (M:M) relationship between entities/models.  
- Have full-CRUD data operations across any combination of the app's models (excluding the User model). For example, creating/reading/updating posts and creating/deleting comments qualifies as full-CRUD data operations. 
- Authenticate users using Django's built-in authentication.
- Implement authorisation by restricting access to the Creation, Updating & Deletion of data resources
- Be deployed online using Railway. Presentations must use the deployed application.


## Planning

In regards to planning, I used a Trello board initially to help me prioritise and write user stories, as well as visualising the progress and having a place to keep my ERD and wireframes.
I used LucidChart for my ERD.
My project had 2 entities additionally to Django’s built in User and used One-to-Many relationships. 

![ERD for project](https://i.imgur.com/aWC4HuSm.png)
![wireframe](https://i.imgur.com/47jwbPam.png)
![wireframe](https://i.imgur.com/3MUqHMAm.png)


## Build Process

I kept a daily log of goals achieved each day to track the project's evolution. 

### Day 0
- Created ERD, Wireframes, and set up Trello.

### Day 1
- Set up the project and created the database.
- Configured both backend and frontend.
- Defined Models, Serializers, and initial viewsets.
- Established initial routes using Django Rest Framework.
- Fetched data via Axios from general views (all users, games, reviews).
- Initiated user creation in the backend.
- Implemented functionalities for Games and Reviews including editing and deletion (backend).
- Started exploring login and logout functionality in Django.


### Day 2
- Worked on login and token generation.
- Implemented logout functionality.
- Encountered issues with CSRF token simulation for endpoint testing, but managed to find a solution.
- Attempted to integrate MUI in the frontend, faced difficulties possibly related to React versions - decided to use React Bootstrap (which I was curious to use anyway)
- Explored setting up react-router, faced obstacles with the latest version and syntax, but followed documentation and was successful in setting up.
- Established a context for sharing initial state pieces.

 
### Day 3
- Focused on the signUp component, sending backend requests for new user creation.
- Started incorporating styling using Bootstrap React components.
- Completed functionality for the SignUp component (creates a new user in the database, navigates to a login page—function integration proved complex).
- Implemented login and logout functionalities.
- Managed cookies for login purposes.


### Day 4
- Continued working on state management, improved data fetching post-login to reduce redundant app fetches for specific users.
- Retrieved and displayed Profile (user) and started working on retrieving Single Game data.
- Added functionality for registering a new game and submitting a review for a specific game.
- Fetched detailed data from a foreign key, created an APIView to retrieve User details related to a specific review.


### Day 5
- Implemented functionalities to delete and edit reviews, sending a post request from the JavaScript frontend to my Python Django-rest-framework backend, using the dynamic built-in capabilities of Django ViewSets. 


### Day 6
- Selected OpenCritic API for retrieving information about existing games, including images.
- Developed functionality for searching games and making API calls to gather game details.
- Restructured the Game Model to accommodate new data formats.
- Completed API-related functionalities.

### Day 7
- Focused on styling aspects, using React Bootstrap, including layout, hover animations, typography, colours, buttons and other small touches.

## Challenges

The biggest difficulty was definitely having to learn how to work with the Django Rest Framework in such a little time - it is quite different from the vanilla full stack django, with it’s use of serializers. To me it felt like quite a big transition having learned how to build a full stack application with Django as part of the course, but then being asked to use React for the frontend and having to use the django-rest-framework. 
 
## Wins

Being successful at using an API which felt perfect for this project, and being able to make it’s functionality work within 1 day including creating new Game instances from it. 

some snippets of code I like:
```
class UserViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # if not authenticated we can't consume API
    def retrieve(self, request, *args, **kwargs): #override the built in one
        instance = self.get_object() #fetches the specific user object based on request
        user_serializer = self.get_serializer(instance)#grabs the serializer for this user
        games_serializer = GameSerializer(instance.game_set.all(), many=True)#creates a specific serializer for all games connected to this user
        reviews_serializer = ReviewSerializer(instance.reviews.all(), many=True)

        response_data = {
            'user': user_serializer.data,
            'games': games_serializer.data,
            'reviews': reviews_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

```

```
 //*CHECKS IF COOKIES ARE SET AND FETCHES DATA BASED ON THAT SPECIFIC USER
    async function checkIfLoggedIn() {
        try {
            if (cookies.user_id) {
                setUserId(cookies.user_id)
                setIsLoggedIn(true)
                const response = await axios.get(`${BACKEND_API}/users/${cookies.user_id}`, {
                    headers: {
                        'Authorization': 'Basic ' + btoa(`${AUTH_USER}:${AUTH_PASS}`),
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                
                setUserId(response.data.user.id)
                setUserGames(response.data.games)
                setUserDetails(response.data.user)
                setUserReviews(response.data.reviews)
            
            }

        } catch (error) {
            console.log('error getting user details', error)
        }
    }
```

## Key Learnings

Learning Python and the Django-rest-framework basics, as well as understanding relational databases. Most of my previous experience was with MongoDB, so using a SQL based database is a very different experience, and there is much that I look forward to learning when it comes to creating relationships between tables and efficiently querying them.

## Known Bugs

Navbar responsiveness on mobile post-login needs improvement.

## Future Improvements

I would like to finish implementing an “average score” for a game based on the scores given on individual reviews (that is why the reviews ask for a score initially, but I did not have time to implement that feature).
I would also like to better organise the frontend code. 
