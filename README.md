# An OlinDB with Roles - Don't blow up your production DB on day1!
Danny Kang, Seungin Lyu

## Inspiration

[A Horror Story](https://www.reddit.com/r/cscareerquestions/comments/6ez8ag/accidentally_destroyed_production_database_on/)
___

Summary : A dev intern at a startup company blew up the production database on day 1 after following the dev environment setup instructions (and accidentally used the production credentials that was used in the instruction).
Incidents like this should be prevented from a systems level, so we are implementing a minimal database with users, roles, and privileges that will prevent any dumb mistake like presented in this Reddit thread.

## Project Description

We are extending the relational database we implemented in homework3 (that supports the shell command line interface and basic queries like SELECT, DELETE, CREATE TABLE, etc)
___

## Goal
    - Create a database assuming that we are running a used-car selling company and we need a database to manage the selling records for each employee
      - Table 1 : Car Table
        - Schema : Primary Key (cid), Car Name, Car Type, Car Price, Car Status, Car name, uid (employee name)
      - Table 2 : User Table
        - Schema : primary key (uid), username, password, roles (customer, employee, manager), revenue generated 
      
      Login :
        - Create user (username, password, role) -> (INSERT INTO USER table (username, password, role))
        -   login command : CarDB -d mydb -U myuser (SELECT from * user table WHERE id = , password = asfawf234)
        - CarDB createUser danny 1q2w3e4r employee

      ## Stretch
      - Table 3 : Roles Table (customer, employee, manager, master)
        - Schema : primary key (rid - role id), privileges
          rid | role_name | privleges
          1      Customer    buy (Car Table)
          2      Employee    Read, Write (Car Table)
          3      manager     Read, Write, Delete (Car Table, User Table)
          4      master      Read, Write, Delete (Car Table, User Table, Roles Table)

          - 1 : buy read + update(only car status) // our design decision
          - 2 : write
          - 3 : delete
          - Customer : Buy
          - Employee : Read, Write
          - Manager : Read, Write, Delete
  
    - Create roles (employee, manager, admin) that has appropriate read/write/delete/update privileges and roles.
    - Create login, logout, create user, create role, grant privilege, etc (postgreSQL style commands)
        - https://alvinalexander.com/blog/post/postgresql/log-in-postgresql-database
        - psql -d mydb -U myuser
___

## Initial Steps
    - Read postgreSQL roles, privileges, users documentation
    - Start implementing users and get users logged in through the shell
___

## Resources
[PostgreSQL databases](https://www.a2hosting.com/kb/developer-corner/postgresql/managing-postgresql-databases-and-users-from-the-command-line?fbclid=IwAR2t0Hv692snhImbs0Ot7DKNpqOfL6akIFjdKH5skiCs2Lvch8qiyKVb6LY)

[Roles](https://www.postgresql.org/docs/9.3/user-manag.html?fbclid=IwAR0jK_Eyxgy3Z6d_naechy-3Tk-atcay_8CQNJSCTpLU7X9-Ddt10DzJj5s)

[Privileges](https://www.postgresql.org/docs/9.3/ddl-priv.html)
___

## Implementation

![Alt text](./DBimage.png?raw=true "Title")
We implemented our program based on command line interface. There are no fancy GUI or pop up features but still, this program manages to provide pretty straightforward and intuitive user experience in terms of navigation and, most importantly, data management. In fact, our program is partly based on homework3 of this course so credits to our instructor Riccardo! We made use of class 'Relation' and some of its methods like 'read/create tuple' to implement database and core functionalities. Our main focus, though, was to implement different **roles** that have varying level of access to data. 

### Roles and privilleges
* Manager
* Employee
* Customer
