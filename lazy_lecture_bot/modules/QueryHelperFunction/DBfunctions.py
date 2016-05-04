# functions to help getting info from table quicker
# I dont exactly know where to put this file in the repo
# so ill just put it next to models.py
# comment if more functions are needed and ill add them


from app.models import *
from django.db.models.query import RawQuerySet

# given video title and user id returns link to video blob
def get_url_to_video(title, user_id):
    video_id = RawQuerySet.raw_query('SELECT video_id FROM videos WHERE user_id = ' + user_id)
    url = RawQuerySet.raw_query('SELECT video_blob FROM videos WHERE video_id = ' + video_id)
    return url


# gets individual transcript segments from table and concatenates them into one string then
# returns it 
def get_transcript_of_user(user_id, video_id):
    full_transcript = ''
    sql_query = 'SELECT transcript FROM videos v, segments s WHERE v.user_id = ' + user_id + ' AND s.video_id = ' + video_id + ' ORDER BY s.segment_id'
    for tran in RawQuerySet.raw_query(sql_query):
        full_transcript += tran
    return full_transcript

# given video title and user id returns the full transcript
def get_transcript_of_video_title(video_title, user_id):
    video_id = RawQuerySet.raw_query('SELECT video_id FROM videos WHERE title = ' + video_title)
    full_transcript =  ''
    sql_query = 'SELECT transcript FROM videos v, segments s WHERE v.user_id = ' + user_id + ' AND s.video_id = ' + video_id + ' ORDER BY s.segment_id'
    for tran in RawQuerySet.raw_query(sql_query):
        full_transcript += tran
    return full_transcript


# given word token returns url link to point in video
def get_token_time_frame(word_id, word_number):
    url_to_video_point = RawQuerySet.raw_query('SELECT word_to_url FROM annotation WHERE word_id = ' + word_id + ' AND word_number = '+ word_number)
    return url_to_video_point

####
# I'll add anymore i can think of here
####
        
