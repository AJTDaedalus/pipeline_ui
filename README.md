<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]

<!-- PROJECT LOGO -->
## Pipeline UI
<p align="center">
  <img src="https://user-images.githubusercontent.com/98370207/158001923-83de168b-587f-43df-bd8c-4abfe016c5b0.png" width="300" height="300">
  </p>  
<br /><br />

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built with</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#deployment">Deployment</a></li>
        <li><a href="#requirements">Requirements</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This project is in support of their growing bioinformatics infrastructure that still relies on command line interaction and a small team of bioinformaticists to manage pipelines and tools.  The goal of this project is to provide a graphical user interface (GUI) to increase accessibility to these pipelines and tools as the bioinformatics portfolio grows.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Docker](https://www.docker.com/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started
### Deployment

#### Dependencies

- Docker
- Python 3.7 environment
- Docker-Compose

#### Deployment Instructions:
*	Recommendation – Select second server for development
*	Ensure dependencies listed above are installed
*	Install Docker in a Python virtual environment
*	Update security features
  * Update “SECRET_KEY” setting as seen in the figure below, to password-like string, preferably randomly generated. https://github.com/AJTDaedalus/pipeline_ui/blob/35602509132c5f50a332ec8ef76a852f45f2ab20/code/settings.py#L12-L23
  * Update “Mail_Server” and “Mail_UserName” in `code/app/__init__.py` as seen in the image below:
    <p align="left">
    <img src="https://user-images.githubusercontent.com/98370207/161188349-fdd6a058-bc85-4e40-b3a6-547f45204137.png" width="325" height="350")
    </p> 
  * Update `docker-compose file` to change the following settings: 
    “MYSQL_ROOT_PASSWORD”, “MYSQL_USER”, and “MYSQL_PASSWORD”
    * Also update “SQLALCHEMY_DATABASE_URI” in `code/settings.py` to match the “MYSQL_USER”, and “MYSQL_PASSWORD” settings to what was used above.
       <p align="left">
       <img src="https://user-images.githubusercontent.com/98370207/161189730-2641341e-7ed6-4e15-860c-53c57dc12cf6.png" width="600" height="100">
       </p>
* Once this is completed, move to the parent folder of the repository where the `docker-compose.yml` file is located and run
  <br />
  the `docker-compose up` command
* Once server is up the IPv4 address can be modified  in the proxy/conf file in the repository  
* Next, Update the administrator in Admin page
  * Register for a new account and make sure to receive email confirmation
  * Log in to the admin page using username “me123@gmail.com” and password “12345678” 
  * Once logged in go to the Admin page and assign admin roles to the newly created admin email account
  * Confirm the new admin user can access the Admin page
  * Remove admin privileges from the “me123@gmail.com” user
* For development only
  * Start up development server using `python main.py` command
        
#### Creating and Testing New Interfaces
* Determine appropriate blueprint to use. NOTE do not use Auth blueprint unless the goal is to allow unconfirmed users without them being re-routed to the “unconfirmed” page.
* Create folder in “app” folder named <Blueprint>
* Create a simple __init__.py file inside newly created folder
* Initialize the new blueprint in the application factory in ` app\__init__.py`
* New blueprints require a `views.py` file
* If the new interface requires the use of Flask-Forms to gather user-submitted information, it is best practice to define those forms in a `forms.py` file inside the associated Blueprint folder
* If new page is being added, add the new routes and necessary forms to that blueprint’s `views.py` and `forms.py` files, respectively
* Note: To add restrictions such as login and permissions requirements, use decorators `@login_required` and `@permission_required(<role>)` above the definition of the route
* Example of Admin Route
  <p align="left">
  <img src="https://user-images.githubusercontent.com/98370207/161361899-43739b7e-96be-42da-940a-f0ffc597795e.png" width="600" height="100">
  </p>
* Next, create the html template and render the template at the bottom of the route created in the `views.py` file using the `render_template` function as seen below.
  <p align="left">
  <img src="https://user-images.githubusercontent.com/98370207/161362138-067eca5d-6bee-4837-9d94-53421876ffb2.png" width="600" height="100">
  </p>
* The new template should extend the base.html
  * Add link to the navigation bar in the `templates\base.html` as seen below
    <p align="left">
     <img src="https://user-images.githubusercontent.com/98370207/161362231-092966b9-7141-42fe-bf9a-7266557b6d81.png" width="600" height="100">
    </p>
  * Per the example above, the `can` function only allows the Admin page to show the user with admin privileges
  * Other restrictions that can be used are: 
    </b>
    User is logged in: (`if current_user.is_authenticated`) or not logged-in (`if current_user.is_anonymous`)
* For testing purposes, it is advisable to use the development server by using `python main.py`. This provides more informative error messages when there is a problem   with the newly introduced code

  
#### Customization
 ##### Adding new pages/functions:
  - Copying and editing blueprints
  - Adding to Navbar
  - Adding access roles
  - Adding new models
  - Initializing blueprint in factory

#### Deploying changes to production:
  - Flask migrate explanation
  - `docker compose up --build` reminder
  
### Requirements
```
pip install -r Requirements.txt
```

### Installation
TBD - installation instructions to be added later

<!-- USAGE EXAMPLES -->
## Usage
TBD - info will be added showing how each page can be used

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Project Link: [https://github.com/AJTDaedalus/pipeline_ui](https://github.com/AJTDaedalus/pipeline_ui)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/AJTDaedalus/pipeline_ui.svg?style=for-the-badge

[contributors-url]: https://github.com/AJTDaedalus/pipeline_ui/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/AJTDaedalus/pipeline_ui.svg?style=for-the-badge
[forks-url]: https://github.com/AJTDaedalus/pipeline_ui/network/members
[stars-shield]: https://img.shields.io/github/stars/AJTDaedalus/pipeline_ui.svg?style=for-the-badge
[stars-url]: https://github.com/AJTDaedalus/pipeline_ui/stargazers
[issues-shield]: https://img.shields.io/github/issues/AJTDaedalus/pipeline_ui.svg?style=for-the-badge
[issues-url]: https://github.com/AJTDaedalus/pipeline_ui/issues
[license-shield]: https://img.shields.io/github/license/AJTDaedalus/pipeline_ui.svg?style=for-the-badge
[license-url]: https://github.com/AJTDaedalus/pipeline_ui/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
