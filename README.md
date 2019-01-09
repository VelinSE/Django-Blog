# Welcome to Recepie, a website about sharing recipes

This application is written in python using **Django v2.1**. Django uses the MVT (Model - View - Template) pattern which is pretty much the same as MVC (Model - View - Controller). The MVC *controller* is the same in MVT, it is just called *view*, and the MVC *view* is called *template* in MVT

The structure of the app as the convention says, each feature is put in a separate folder, with its own urls, models, templates, vies (controllers), forms, migrations ect.

---

## Link to the live application - [Recepie](https://ledjango.herokuapp.com/)
 

 ## Usable account you can experiment with 
| Type       | Username | Password   |
|------------|----------|------------|
|Normal user | normal   | logmein123 |
|Superuser   | teacher  | logmein123 |

## CORE FUNCTIONALITIES
* ###### Blade Usage
    Or in our case ```Django template language```. Examples of it can be found in the **templates** directories located in recepie and in blog folders. We are using base.html as the general template, and all the other files extend it, as kind of patial views.
* ###### Routes
    The router is the first layer that handles requests, based on the requested url it determins which view (controller) to call. The main routes can be found in **recepie/urls.py**.

* ###### Authentication
    We have implemented the conventional authentication, meaning login with username and password. We have added *change password* and  *forgotten password* functionalities. There is also social authentication, currently we support **Google**, **GitHub**, and **Facebook** login. Moreover, when you login with social auth, the provider gives us a username, then when the user visits the change password page for the time the user can set a password, and later can login with both the social auth and the provided username with the set password. If he then goes to change the password again the user will be asked to enter the old one. 

* ###### Authorization
    When using Django with the built in User model, or with a custom one that follows certain rules, the django **[admin](https://ledjango.herokuapp.com/admin)** page can be used. Is a short summary, there are roles and permission as well as two fields (is_superuser, is_staff) which are important. The roles and and permissions are the same as anywhere else, however the two fields are also important. A user that has *is_staff* set to *true* can login in the admin page, a user that has *is_superuser* set to *true* has all existig permissions. A *staff* can have in general 4 permissions (CRUD) for each existing model, he can login in the admin and administer data for the models that has permissions for. We have also defined some custom perissions to satisfy our needs, **view_original_img** and **run_exports**, the functionality that they authorize is not in the admin panel, but in the actual site. For more informaion keep reading, they will be discussed later in other sections.
* ###### Migrations
    As described in the basic app structure there are migrations the models of each of the features (and for some models in the 3rd party packages), our migrations can be found in **recepie**, **blog** and **rest** */migartions*

* ###### Seeds
    Seeds can be created usign the command ``python manage.py dumpdata FIXTURE ``, that gets the data from the database, specific feature and even model can be selected, and put the data into a so-called fixture. In our case we have one fixture which is a *.json* file. The data from the fixture can be inserted in the database using another command ``python manage.py loaddata FIXTURE ``

* ###### CRUD-operations for users
    In our systems users have:
    * Profile picture
    * Username
    * First name
    * Last name 
    * Password 

    We provaide the functionality to change everything except for the username. There is server side validation of the forms, `form.is_valid()` for the POST and in some cases there is validation for the GET. All POST forms have `CSRF` protection. 

* ###### CRUD-operations for content
    Our recipes have:
    * Title
    * Content (recipe instructions)
    * Cooking time
    * Number of servings
    * Image
    * Thumbnail image
    * Ingredients
        * Name 
        * Metric 
        * Quantity

    Everything in the recipe can be changed.

* ###### CR-operations for files
     Image for both users and posts are available. Users can change only their own profile image and the images of their own posts. The profile image and the post thumbnail can be seen by everybody. The original post image can be seen only by its creator, or by a user with the **view_original_img** permission.

* ###### Image manipulation 
    We have server-side manipulation of the blog images. When the user uploads an image it is stored as original image. During the upoad a copy of the image is made, it is resized and saved as a thumbnail.

* ###### Export users to Excel 
    We have an Excel export in the profile section, it is only visible to those users that have **run_exports** permission. 
    The included data in the export is:
    * User ID
    * Last Login
    * Is Superuser
    * Username
    * First name 
    * Last name 

* ###### Export content to PDF
    A recipe can be printed by a visitor of our website. Printed recipe is a simple html file, that can be downloaded.
    Included data:
    *  Recipe name
    *  Cooking time
    *  Servings
    *  Ingredients
    *  Instructions(content)

* ###### API Users
    API supports full CRUD operations for users. Currently, it's available only to administrators
* ###### API Content
    API supports full CRUD operations for users. Available to all users, however, reasonably only authors can edit their recipes

* ###### API Endpoints
* https://ledjango.herokuapp.com/api/ - API Root
* https://ledjango.herokuapp.com/api/users/ - Users
* https://ledjango.herokuapp.com/api/posts/ - Posts

* ###### 3rd party package usage
    * PIL -> Image manupulation
    * Weasyprint -> PDF exports
    * XlsxWriter -> Excel exports
    * Ckeditor -> Post content input
    * Rest_framework -> API
    * Social_django -> Social media authentication 

* ###### Extra 
    One of our extras is the server-side filer, which checks for a given string in the post Title and Content.