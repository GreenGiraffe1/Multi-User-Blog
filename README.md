# Matt's Blog

**Multi-User-Blog** is a blogging platform designed to be hosted on Google App Engine. User's can securely sign-up, login, create posts, comment on posts, and like posts. The platform provides appropriate user permissions and security measures.

Click here to be taken to [Matt's Blog's implementation of this platform](http://hello-world-156422.appspot.com).

## Setup:
Begin the setup by cloning all files to the same directory, and making sure that Python 2.7x is installed. You'll need to create a new Google Cloud Platform Console project or retrieve the project ID of an existing project from the Google Cloud Platform Console. Then install and then initialize the Google Cloud SDK.

Detailed Instructions can be found here:
[Google App Engine Documentation](https://cloud.google.com/appengine/docs/python/getting-started/creating-guestbook)

## Usage:

The blogging platform can be run locally as well as in the Google Cloud / App Engine. This should be done primarily for testing changes and debugging. Google Cloud will provide your application with persistent storage, a consistent web address, and the ability to handle traffic at volume.

#### Deploying to Local Server:

In the terminal navigate to the directory where the cloned files are located and run the following command:

`dev_appserver.py app.yaml`

This will deploy your application locally. You can access it by typing http://localhost:8080 in your browser. The terminal window will now log all the interactions of this local server which is helpful for debugging.

For additional information visit: [Using the Local Development Server](https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server)

#### Deploying to Google App Engine:

Navigate to the directory where the cloned files are located and run the following command in the terminal:

`glcoud app deploy`

The first time you run this command it may take up to 15 minutes. Eventually you'll be asked to whether you'd like to deploy you app, enter "y" for yes. After a few more minutes of waiting you should see a success message, and the URL to the blogging platform will be displayed.

For additional information visit: [Deploying a Python App](https://cloud.google.com/appengine/docs/standard/python/tools/uploadinganapp)

Admin functions can be accessed from the [Google Cloud Platform Dashboard](https://console.cloud.google.com/home/dashboard). (You'll need to be logged in to you Google account.)

## Attribution

This project was written while I was taking the Udacity Full-Stack Nanodegree, and significant chunks of the structure / ideas behind the structure were provided by the course author.


## License

**Multi-User-Blog** is a public domain work, with license
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
