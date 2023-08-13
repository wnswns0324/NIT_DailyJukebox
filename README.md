# NIT_DailyJukebox
Python, Spotify API, Instagrapi Based Daily track recommender.

Installing Libraries:
> pip install python-dotenv

> pip install requests

> pip install firebase-admin

Change Values in .env file

Currently working on improving its stability

Firebase DB Holds IDs of users that receive DM when new playlist is uploaded.
***Tag List***
> usercount, count, ID_tag

> ex) {"usercount":3}, {"count":2}, {"1","First ID"}, {"2","Second ID"}, {"3","Third ID"}
>> In the Above example, the playlist count will be 2, so next upload will be album image of "Jazz_2", "POP_2", "EDM_2". The python code main.py will auto update the value when playlist is uploaded.

> Currently Working on DM user control
