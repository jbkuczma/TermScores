# TermScores
Quickly and easily check NHL, NBA, and NFL scores from your command line.

# Requirements
    Python3 and requests are required.
# Usage
Navigate to the directory where you save the source code to and run:

    python3 scores.py [league] [date]
    
  To retrieve NHL scores from Feburary 12, 2016:
        
        python3 scores.py -nhl 2/12/2016

          MONTREAL vs BUFFALO
          MTL => 4| Shots: 30
          BUF => 6| Shots: 22
          Period: FINAL
          ===================
          LOS ANGELES vs NY RANGERS
          LAK => 5| Shots: 34
          NYR => 4| Shots: 28
          Period: FINAL OT
          ===================
          PITTSBURGH vs CAROLINA
          PIT => 2| Shots: 26
          CAR => 1| Shots: 30
          Period: FINAL SO
          ===================
          COLORADO vs DETROIT
          COL => 3| Shots: 21
          DET => 2| Shots: 45
          Period: FINAL SO
          ===================
          NASHVILLE vs TAMPA BAY
          NSH => 3| Shots: 30
          TBL => 4| Shots: 28
          Period: FINAL OT
          ===================
          ST LOUIS vs FLORIDA
          STL => 5| Shots: 28
          FLA => 3| Shots: 32
          Period: FINAL
          ===================
          CALGARY vs ARIZONA
          CGY => 1| Shots: 27
          ARI => 4| Shots: 35
          Period: FINAL
          ===================
          
  Also a convenient check what games are playing in the future:
        
      python3 scores.py -nhl 3/2/2016
      
        TORONTO vs WASHINGTON
        TOR => 0| Shots: 0
        WSH => 0| Shots: 0
        Period: 7:00 PM
        ===================
        CHICAGO vs DETROIT
        CHI => 0| Shots: 0
        DET => 0| Shots: 0
        Period: 8:00 PM
        ===================
        MONTREAL vs ANAHEIM
        MTL => 0| Shots: 0
        ANA => 0| Shots: 0
        Period: 10:00 PM
        ===================
# To Do
  
* Fix NBA score retrieval 
  
* Add NFL score retrieval
  
* Possibly expand into other sports
  
* Improve README

* Add screenshots of outputs to show color

* Create requirements.txt
  
  
