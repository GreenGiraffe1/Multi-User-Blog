# Matt's Blog

**ND_multi-user-blog** is a blogging platform designed to be hosted on Google App Engine. User's can securely sign-up, login, create posts, comment on posts, and like posts. The platform provides appropriate user permissions and security measures.

### Setup:
Begin the setup by cloning all files to the same directory, and making sure that Python 2.7x is installed. You'll need to create a new Google Cloud Platform Console project or retrieve the project ID of an existing project from the Google Cloud Platform Console. Then install and then initialize the Google Cloud SDK.

###### Detailed Instructions:
[Google App Engine Documentation](https://cloud.google.com/appengine/docs/python/getting-started/creating-guestbook)

### Usage:

Once you have Google App Engine setup, navigate to the directory where the files are located and run the following command in the terminal:

`glcoud app deploy`

The first time you run this command it may take up to 15 minutes. Eventually you'll be asked to whether you'd like to deploy you app, enter "y" for yes. After a few more minutes of waiting you should see a success message, and the URL to the blogging platform will be displayed.

Admin functions can be accessed from the [Google Cloud Platform Dashboard](https://console.cloud.google.com/home/dashboard).

### Attribution

This project was written while I was taking the Udacity Full-Stack Nanodegree, and significant chunks of the structure / ideas behind the structure were provided by the course author.


### License

**ND_multi-user-blog** is a public domain work, with license
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
