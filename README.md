# Helsinki Genomic Graph Archive

![GitHub Actions](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/workflows/CI/badge.svg)
![codecov](https://codecov.io/gh/Helsinki-Genomic-Graph-Database/HGGD/branch/main/graph/badge.svg?token=Ft06460tNh)

Helsinki Genomic Graph Database is a database for the University of Helsinki researchers to add graph datasets of genomic sequences. The graphs and the script files will be available for download on a web page along with some metadata of the datasets and graphs.

## Project progress

Program is running on [production server](https://hggd.cs.helsinki.fi/index)

[Product Backlog](https://docs.google.com/spreadsheets/d/1jQ1yPn0-mzYhNJW9QTR2Ywo7aS68i67zV4ff8tXcJfQ/edit#gid=1289730588)

[Sprint Backlog](https://docs.google.com/spreadsheets/d/1jQ1yPn0-mzYhNJW9QTR2Ywo7aS68i67zV4ff8tXcJfQ/edit#gid=0)

[Presentation video](https://www.youtube.com/watch?v=prDzgknSgZ0) (no sound)

## Documentation

[User manual](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/user_manual.md)

[Accessing and setting up the production server](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/production_server.md)

[Architecture document](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/architecture.md)

[Development manual](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/development_manual.md)

## Definition of Done

* All acceptance criteria is met
* Everything concerning datasets is tested with unittests throughly with test data provided by the client
* Quality of code is tested by pylint with a score of at least 8
* Feature is pushed to main branch through the CI/CD pipeline
* Feature is in production or staging server

## Working practices

[Working hours](https://docs.google.com/spreadsheets/d/1jQ1yPn0-mzYhNJW9QTR2Ywo7aS68i67zV4ff8tXcJfQ/edit#gid=2009419284) 9.00-15.00 in DK107 unless otherwise agreed.

Daily scrum every day at 9.00. Client meetings (Sprint review) on Mondays at 10.00 (from sprint 3 onwards client meetings will be on Thursdays at 10.00), retrospectives and next sprint planning after the meeting.

Everything documented in English.

### Branching

Everything is pushed to main branch. Only working code!

### Workflow

* Choose task from Sprint backlog, tag your name and mark working status.

* Pull from main -> Code and write tests -> Test on own computer -> Fix issues -> Pull from main -> Test again on own computer -> Fix issues -> Push to main.

* When done, mark status as done and write down hours in backlog.
