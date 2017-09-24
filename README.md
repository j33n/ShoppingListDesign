![Alt text](https://travis-ci.org/JeanAbayo/ShoppingListDesign.svg?branch=addingflask "TravisCI status")
[![Coverage Status](https://coveralls.io/repos/github/JeanAbayo/ShoppingListDesign/badge.svg?branch=master)](https://coveralls.io/github/JeanAbayo/ShoppingListDesign?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c1da0b83a0f345909e869693ddc60664)](https://www.codacy.com/app/JeanAbayo/ShoppingListDesign?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JeanAbayo/ShoppingListDesign/&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/c1da0b83a0f345909e869693ddc60664)](https://www.codacy.com/app/JeanAbayo/ShoppingListDesign?utm_source=github.com&utm_medium=referral&utm_content=JeanAbayo/ShoppingListDesign/&utm_campaign=Badge_Coverage)
<a href="https://shoppinglistdesigns.herokuapp.com/">
    <img src="app/static/images/sl_logo.png" alt="ShoppingList logo" title="ShoppingList" align="right" height="60" />
</a>

ShoppingList
======================

ShoppingList makes shopping quick, easy and fun allowing users to add, update, view or delete items in a shopping list and share the lists with the public.
![My homepage screen](Designs/screenshot.png?raw=true "My homepage screen")
Here is a link to my ShoppingList app
<a href="https://shoppinglistdesigns.herokuapp.com/">ShoppingList</a>

### Prerequisites

I am using basic CSS, bootstrap and jQuery for the template and
at the backend I am using Flask

### Installing

To get up and running with it, just clone this repository, switch in that folder then setup flask and finally run the flask server.
Also set environment variables from repository settings

```
git clone https://github.com/JeanAbayo/ShoppingListDesign.git
cd ShoppingListDesign
export APP_SETTINGS="config.DevelopmentConfig"
virtualenv venv
source dir/to/venv/bin/activate
pip install -r requirements.txt
python manage.py

```
To run tests
```
export APP_SETTINGS="config.TestingConfig"
nosetests tests.py

```

## Authors

* **Jean Abayo** - *Initial work* - [JeanAbayo](https://github.com/JeanAbayo)

## Credits

* **Daisy Ndungu** - [DaisyNdungu](https://github.com/daisyndungu)
* **Humphrey Musonye** 
