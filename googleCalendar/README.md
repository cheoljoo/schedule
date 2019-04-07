# Description
- copy heal2u/* .    to use heal2u account

## command to insert as an input into google calendar
- python3 insert.py
    - Number of WorkContents ; Now is 1(Start),2(End) ; Count of 30 Mins ; Messages =>
        - choose # of WorkContents
        - choose 1 or 2  (ex. 1 is that current time is start time)
        - counts of 30 minutes (ex.  5 is 5*30 min ( 2 hours 30 minutes)
        - Messages 
```
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
```

- input example => 
    - 11 ; 1 ; 4 ; TTT
        - calendar => preparation - TTT   from current time  to time + 2 hours
    - 0 ; 2 ; 3 ; 
        - calendar => email check - TTT   from current time - 1 hour 30 min  to current time

## make statistics each month (normal bar and pie style)
- python3 statistics.py
    - statistics.py -y <year> -m <month>
- ex) python3 statistics.py -y 2019 -m 4
    - deliverables
        - 2019-04-short.yaml
        - 2019-04-long.yaml
- where can you show the result : 
    - https://heal2u.github.io/bar-chart/
    - https://heal2u.github.io/pie-chart/
    - https://heal2u.github.io/data/bar-chart.json
    - https://heal2u.github.io/data/pie-chart.json
- d3.js : ./chart
    - ./chart/_data/bar_chart.yaml  : take care of file name
    - ./chart/data/bar_chart.json
    - ./chart/bar_chart/index.html
    - ./chart/pie_chart/index.html
    - reference
        - [Bar Chart : D3.js Visualizations Using YAML and Jekyll](https://apievangelist.com/2016/09/20/d3js-visualizations-using-yaml-and-jekyll/)
        - [Pie Chart : D3.js Visualizations Using YAML and Jekyll](http://d3.js.yaml.jekyll.apievangelist.com/pie-chart/)

## make statistics each year (stacked style)
- python3 year_statistics.py
    - year_statistics.py -y <year> -m <month>
- ex) python3 statistics.py -y 2019 -m 4    : get statistics until 2019/04
    - deliverables
        - 2019-short.json
        - 2019-long.json
- where can you show the result : 
    - You can not see the proper result in github. But you can see the result in jekyll developing environment.
        - http://localhost:4000/stacked/
    - ![Stacked_Bar_Chart](https://github.com/cheoljoo/schedule/blob/master/images/2019-04-07_stacked.png)
- d3.js : ./stacked_bar_chart
    - ./stacked_bar_chart/data/2019-short.json
    - ./stacked_bar_chart/stacked/index.html
    - reference
        - [Stacked Bar Chart Original Example](http://bl.ocks.org/jamesleesaunders/ac5b6134ad7144e8327d)
        - http://bl.ocks.org/mstanaland/6100713

