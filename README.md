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
      - Schema : Name of Employee, Number of Cars Sold, Revenue Generate, etc.
    - Create roles (employee, manager, admin) that has appropriate read/write/delete/update privileges and roles.
    - Create login, logout, create user, create role, grant privilege, etc (postgreSQL style commands)
___

## Initial Steps
    - Read postgreSQL roles, privileges, users documentation
    - Start implementing users and get users logged in through the shell
___

## Resources
[PostgreSQL databases](https://www.a2hosting.com/kb/developer-corner/postgresql/managing-postgresql-databases-and-users-from-the-command-line?fbclid=IwAR2t0Hv692snhImbs0Ot7DKNpqOfL6akIFjdKH5skiCs2Lvch8qiyKVb6LY)

[Roles](https://www.postgresql.org/docs/9.3/user-manag.html?fbclid=IwAR0jK_Eyxgy3Z6d_naechy-3Tk-atcay_8CQNJSCTpLU7X9-Ddt10DzJj5s)

[Privileges](https://www.postgresql.org/docs/9.3/ddl-priv.html)
