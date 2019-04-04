# How to
- copy heal2u/* .    to use heal2u account
- python3 insert.py
    - Number of WorkContents ; Now is 1(Start),2(End) ; Count of 30 Mins ; Messages =>
        - choose # of WorkContents
        - choose 1 or 2  (ex. 1 is that current time is start time)
        - counts of 30 minutes (ex.  5 is 5*30 min ( 2 hours 30 minutes)
        - Messages 

==WorkContents==
0 email check
1 email detailed check
2 github
3 calendar check / somedaytalk gmail
4 somedaytalk
5 seminar local
6 code document
7 code design
8 code review
9 code analysis
10 ps
11 preparation
12 learningnet
13 opensource
14 management document
15 management report
16 management interview
17 management review
18 meeting weekly
19 meeting review
20 meeting management
21 meeting followup
22 scrum

- input example => 
    - 11 ; 1 ; 4 ; TTT
        - calendar => preparation - TTT   from current time  to time + 2 hours
    - 0 ; 2 ; 3 ; 
        - calendar => email check - TTT   from current time - 1 hour 30 min  to current time

