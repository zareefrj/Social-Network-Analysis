# **Twitter Scraper Bot**

**List of functions**
1. `Scraper.fetch_userinfo(username)`

Returns a dictionary of the user's Twitter information as below (username should not contain "@"):
``` py
{
    'name': 'Anwar Ibrahim',
    '@': '@anwaribrahim',
    'bio': 'Perdana Menteri Malaysia ',
    'userLocation': 'Malaysia',
    'joinDate': 'Joined March 2007',
    'verified': True,
    'followings': '12.6K',
    'followers': '1.8M'
}
```

2. `Scraper.fetch_followings(username, limit=50)`

Returns a Numpy Array of the user's followings (in @'s) as shown below (username should not contain "@"):
``` py
array(['@501Awani', '@AdamAdli', '@SinarOnline', '@SyedSaddiq',
       '@bernamadotcom', '@drwanazizah', '@fahmi_fadzil', '@hannahyeoh',
       '@kuasasiswa', '@malaysiakini'], dtype='<U14')
```

3. `Scraper.fetch_followers(username, limit=50)`

Returns a Numpy Array of the user's followers (in @'s) as shown below (username should not contain "@"):
``` py
array(['@501Awani', '@AdamAdli', '@SinarOnline', '@SyedSaddiq',
       '@bernamadotcom', '@kuasasiswa', '@malaysiakini'], dtype='<U14')
```

4. `Scraper.get_posts(query, filters=None, limit=10)`

Returns a Pandas DataFrame of the posts based on your query as shown below:
```
	Twitter Username	Post	Date Posted
0	@2nakanski	Sheraton? Ermmm I hardly know her	Jun 11
1	@75edebb37a6c430	This new grouping proves Sheraton Move is a sh...	Jun 4
2	@777eilwek1	Sheraton?	Jun 7
3	@AGiannas	It is in Ethiopia . Sheraton here shows prices...	Jun 7
4	@AdLib716	@HeidiLiberatore and I had our wedding recepti...	Jun 9
```

<hr>

# **Twitter Search Filters**

1. `to:`
   
   Filters tweets sent to a specific user.
   
   *Example: to:username*

2. `from:`
   
   Filters tweets sent from a specific user.
   
   *Example: from:username*

3. `filter:nativeretweets`
   
   Filters native retweets, excluding retweets with comments.
   
   *Example: filter:nativeretweets*

4. `filter:replies`
   
   Filters replies to a specific tweet or user.
   
   *Example: filter:replies*

5. `filter:links`
   
   Filters tweets containing links.
   
   *Example: filter:links*

6. `since:`
   
   Filters tweets posted since a specific date. The date should be in the format "YYYY-MM-DD".
   
   *Example: since:2022-01-01*

7. `until:`
   
   Filters tweets posted until a specific date. The date should be in the format "YYYY-MM-DD".
   
   *Example: until:2022-12-31*

8. `-filter:`
   
   Excludes specific search criteria.
   
   *Example: -filter:retweets* **(excludes retweets)**

9. `min_retweets:`
   
   Filters tweets with a minimum number of retweets.
   
   *Example: min_retweets:1000*

10. `lang:en`
    
    Filters tweets in a specific language. "en" represents English.
    
    *Example: lang:en*

11. `filter:safe`
    
    Filters tweets marked as "safe" content.
    
    *Example: filter:safe*

12. `min_faves:`
    
    Filters tweets with a minimum number of favorites.
    
    *Example: min_faves:500*

You can use these filters in combination to create more specific search queries. Remember to replace "username" with the actual Twitter username you want to filter by and adjust the dates and numbers as needed for your search requirements.

**Sample Combined Query**
``` py
posts = scraper.get_posts(query="#LangkahSheraton OR sheraton OR #SheratonMove OR \"langkah sheraton\"", filters="-filter:links since:2020-01-09 lang:en -filter:nativeretweets", limit=500)
```