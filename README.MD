![PUPFINDER](./client/pupfinder-front/src/assets/PUPFINDER.png)

### A revolutionary solution for dog shelters and stalkers

Have you ever seen a cute dog on the street and thought "Man, I wish I could just take it home"?
Well, now you can!

Our powerful service allows you to instantly check your neighborhood for any reported homeless dogs, wherever you are, 
whenever you are.

Can't deal with any more muzzles to fill? Do something good for the pupper and report it, so that
someone else may pick it up instead!

### Quick start

As an unauthenticated user, you will be able to access the home page and search for new puppers.
To start, enter your current location in the search map or just click on it to precisely establish 
the place.

You can search for dogs there either by clicking Enter, or pressing on the button Go to location.
If you wish to identify a puppy, hover your mouse over a chosen marker to see its photo and basic 
information about it. You can also look for puppies chronologically, by clicking on the button with
a specific id.

The spot you have chosen can also be used to report a puppy. However, in order to use it you have to login.
(If you have no account, you have to register beforehand). You can also log out later by clicking on the appropriate button.

### Main functionalities

- Authentication: User registration, login, logout
- New dog report
- Centering map on a marker
- Adding markers for dogs
- Displaying a dog picture

### Main technologies
- Vue,
- FastAPI,
- MySQL

### Available API Endpoints

#### POST /api/auth/token/

An endpoint necessary for authentication. 
Takes as parameter form data compliant with OAuth2PasswordRequestFormat, as defined by FastAPI, and returns a valid token with a predefined expiration date, after which another authentication will be necessary. Returns 400 in case of unsuccessful authentication.

#### POST /api/owners/

An endpoint set up to create a new owner after registration. Accepts form data compliant with registration data and creates a new user with appropriate credentials. Returns new model username as a proof of successful transaction. After this action, the new user will be able to log in under provided here username and password.

#### GET /api/dogs/

Returns a list of all dogs in the viccinity of the provided location, as well as the list of their recent sightings.  

#### POST /api/dogs/

Accepts a form with the report of a new dog and adds the dog to the database, registering a new photo and sighting as well. Returns the dog and sighting models as proof.

#### GET /api/dogs/{dog_id}/photo/

Accepts a dog id as parameter and returns its photo from the database, if it exists, in the form of a streaming png file. 

#### POST /api/photo/

Accepts a provided photo file (in the format of UploadFile) and saves it on the backend, returning just url to the saved file (so that it can be later added to the database).


![Components](./server/puppies/components.jpg)

![AuthenticationFlow](./server/puppies/authflow.png)

