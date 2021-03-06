# A Database with Roles - Don't blow up your production DB on day 1!
Danny Kang, Seungin Lyu

## Inspiration

[A Horror Story](https://www.reddit.com/r/cscareerquestions/comments/6ez8ag/accidentally_destroyed_production_database_on/)
___

Summary : A dev intern at a startup company blew up the production database on day 1 after following the dev environment setup instructions (and accidentally used the production credentials that was used in the instruction).
Incidents like this should be prevented from a systems level, so we are implementing a minimal database with users, roles, and privileges that will prevent any dumb mistake like presented in this Reddit thread.

A few solutions we suggest :

- Backup
- Database Roles and Privileges
- Row-Level Security
- Stay away from
  ```
  DROP TABLE table_name;
  DROP DATABASE database_name;
  DELETE * FROM TABLE WHERE 1=1;
  ```
Please take a look at the [slides](https://docs.google.com/presentation/d/1REns_PbwlnRoOVgmzZO2bhEqes41cJcaX9RZv7D_DuU/edit?usp=sharing) we used for our final presentation for more details.

## Roles
Role: a database user, or a group of database users (depends on the setup)
“Roles can own database objects (tables) and can assign privileges on those objects to other roles to control who has access to which objects” (PostgreSQL)
```
CREATE ROLE name; 
DROP ROLE name;
CREATE ROLE name LOGIN (CREATE USER name)
GRANT group_role TO role1, ... ;
REVOKE group_role FROM role1, ... ;

```
## Privileges
```
GRANT { { SELECT | INSERT | UPDATE | DELETE | RULE | REFERENCES | TRIGGER }
    [,...] | ALL [ PRIVILEGES ] }
    ON [ TABLE ] tablename [, ...]
    TO { username | GROUP groupname | PUBLIC } [, ...] [ WITH GRANT OPTION ]

```
## Row-Level Security (RLS)
  ### Concept
  RLS supports two types of security predicates.
  “Filter predicates silently filter the rows available to read operations (SELECT, UPDATE, and DELETE)”
  “Block predicates explicitly block write operations (AFTER INSERT, AFTER UPDATE, BEFORE UPDATE, BEFORE DELETE) that violate the predicate”
  ### Use Cases 
  "A hospital can create a security policy that allows nurses to view data rows for their patients only."
  "A bank can create a policy to restrict access to financial data rows based on an employee's business division or role in the company."

## Project Description

We are extending the relational database we implemented in homework3 (that supports the shell command line interface and basic queries like SELECT, DELETE, CREATE TABLE, etc). We made a car sales DB with three roles and two tables (Cars, Users)It's not entirely query based, but you get the idea.
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
Following is the list of roles and their privilleges. Essentially, there are 3 roles where manager has full power over manipulation of data, employees have limited power over data, and customers can only view limited data. This structure prevents roles with lower authority to change data, which is desirable as far as security is concerned. 

* **Manager**: have access to create, read, update, and delete
* **Employee**: have access to only read and update
* **Customer**: have access to only read (but can not view certain data that are related to privacy such as the relation 'Users')

### CRUD operations
Following table summarizes the privilleges of each role in our program.
```
Role_Table = {
"Manager": ["Create", "Read", "Update", "Delete"],
"Employee": ["Read", "Update"],
"Customer": ["Read"]
}
```
Implementation of create, read, and delete operations were done directly using methods in the class 'Relation' that we implemented for homework3. So after program gets necessary input from users, the program gives those information as arguments to those methods to reflect expected changes in database. Update operation was implemented by using both delete_tuples and create_tuple so that the tuples that user wants to change is initially deleted and re-created with changed values. 

### Database
The back-end of our program lies databases that are in form of several relations as shown below. 
```
USERS = Relation(["name", "id", "password", "role", "number of cars sold", "sales"],
["id"],
[
("Danny", "kdy304g", "1234", "Manager", 0, 0),
("Seungin", "teamoji", "1234", "Manager", 0, 0),
("Sam", "2", "1234", "Manager", 0, 0)]
```
Whenever changes are made by either manager or employee, the changes are immediately reflected in the program within corresponding relation. Whereas operations such as create and delete completely create or delete a tupels, other operations partially affects some values within a designated tuple. 

### User Experience(flow of execution)
Once the program launches, users can either **log in** or **create new account**. Once the user inputs appropriate info to log in, "log in successful!" message appears and users can choose the **relation**  that they want to make changes. Once the choice is made, appropriate **menu** pops up according to different roles that users might have.  For example, while manager role can choose from any relations and any CRUD operations, customer role has severly limited  option. The detail of our implementation is that if customer attempts to view information of other users, "access denied"  message pops up to deny the user's attempt to view other users' private info such as password. Also, customers have to input select query to view data they want. 
```
option = input("Choose from menu: ")
if option == "1":
    try:
        s = input("Input Select Query : \n")
        if(s.find("Users") != -1):
            print()
            print("Access Denied!!\n")
        else:
            aq = parseQuery(s)
            q = convert_abstract_query(db, aq)
            r = evaluate_query(q)
            print(r)
    except Exception:
        print("Invalid Query")
```
___
