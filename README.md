# NIT_DailyJukebox

Python, Spotify API, Instagrapi Based Daily track recommender.

Installing Libraries:

```bash
pip install -r requirements.txt
```

Change Values in .env file

Currently working on improving its stability

Firebase DB Holds IDs of users that receive DM when new playlist is uploaded.
**_Tag List_**

```
{ usercount:(user count) },
{ count: (genre count) },
{ (user squence id1): (user id1) }
{ (user squence id2): (user id2) }
{ (user squence id3): (user id3) }
(...)
```

> ex) {"usercount":3}, {"count":2}, {"1","First ID"}, {"2","Second ID"}, {"3","Third ID"}
>
> > In the Above example, the playlist count will be 2, so next upload will be album image of "Jazz_2", "POP_2", "EDM_2". The python code main.py will auto update the value when playlist is uploaded.

> Currently Working on DM user control
