# Coronavirus analysis

This repo analyzes all the 1.1 Billion geotagged Tweets sent in 2020 to track the "spread" of Coronavirus on Twitter.

To analyze this huge dataset, the partition-map-reduce paradigm is used. The tweets are first partitioned by day, after which the tweets sent on any one day are mapped by the country of origin and language of the tweet. Next, after the tweets from all 366 days have been mapped, all the extracted data is "reduced" into one file for the country of origin of the tweet, and one file for the language of the tweet. Finally, these "reduced" files are split up by the hashtags cotained inside each tweet to make it easier to visualize how many tweets were sent from each country and in which languages.

Not surprisingly, it was observed that the USA was sending out the most Coronavirus Tweets, followed by India. And, of course, a large majority of the Tweets were sent in English.
