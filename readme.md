# Project Q - Quartermaster

Project Q is a tools that tracks for malicious activities on systems using OS Query and uses Sophos Intellix APIs to 
check if they are malicious. Project Q will cache the results Intelix APIs to save on query time and money. 

## Getting started

### Prerequisites
* You know how to setup Kafka, OS Query
* You need to have [Sophos Intelix API](https://api.labs.sophos.com/doc/index.html) credentials 

### Installing
* You need to have a Kafka server running <enter details>
* You need to install and OS query with the configs we have included in osquery/ <insert os query link>
* To start the docker container run make file after setting django secret key.
* you can create a superuser by bash-ing into the container, cd to project directory and running
    ```
    python3 manage.py createsuperuser
    ```

Once you have everything setup, you can see the events in UI Dashboard

You can link to DB instead of local mysqlite.

## License
This project is licensed under Apache License, Version 2.0. See the LICENSE file for full license text.

#### Acknowledgements
* [Sophos Intelix API](https://api.labs.sophos.com/doc/index.html)
* [OS Query](https://osquery.io/)
* UI Theme [Atlantis-Lite](https://github.com/themekita/Atlantis-Lite) by themekita
