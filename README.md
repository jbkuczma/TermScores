# TermScores
Quickly and easily check NHL, NBA, and NFL scores from your command line.

# Requirements
    Python3 is required
    
    
# Usage
    
Download the source code, change to its directory, and run:
    
    pip install -r requirements.txt
    
    python3 termscores.py [league] [date]
    
  Retrieve NHL scores from Feburary 12, 2016:
        
        python3 termscores.py -nhl 2/12/2016

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
          
Retrieve NBA scores from Feburary 23, 2016:
        
        python3 termscores.py -nba 2/23/2016
        
          'Magic vs 76ers'
          'ORL => 33|34|30|27|124'
          'PHI => 31|31|31|22|115'
          'Final'
          '=============================='
          'Pelicans vs Wizards'
          'NOP => 19|32|14|24|89'
          'WAS => 24|30|31|24|109'
          'Final'
          '=============================='
          'Kings vs Nuggets'
          'SAC => 28|33|30|23|114'
          'DEN => 25|25|27|33|110'
          'Final'
          '=============================='
          'Rockets vs Jazz'
          'HOU => 28|33|30|23|114'
          'UTA => 25|25|27|33|110'
          'Final'
          '=============================='
          'Nets vs Trail Blazers'
          'BKN => 21|28|33|22|104'
          'POR => 34|29|22|27|112'
          'Final'
          '=============================='
            
  Also a convenient check what games are playing later in the season:
        
      python3 termscores.py -nhl 3/2/2016
      
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
        
    python3 termscores.py -nba 3/1/2016
    
        'Suns vs Hornets'
        'Tipoff at 7:00 pm ET'
        '=============================='
        'Bulls vs Heat'
        'Tipoff at 7:30 pm ET'
        '=============================='
        'Trail Blazers vs Knicks'
        'Tipoff at 7:30 pm ET'
        '=============================='
        'Magic vs Mavericks'
        'Tipoff at 8:30 pm ET'
        '=============================='
        'Hawks vs Warriors'
        'Tipoff at 10:30 pm ET'
        '=============================='
        'Nets vs Lakers'
        'Tipoff at 10:30 pm ET'
        '=============================='
# To Do
  
* ~~Fix NBA score retrieval~~ 
  
* Add NFL score retrieval
  
* Possibly expand into other sports
  
* Improve README

* Add screenshots of outputs to show color

* ~~Create requirements.txt~~

* Clean up code
  
  
