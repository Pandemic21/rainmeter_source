import praw
import time


def get_entry_exists(submission_id):
	for key in d.keys():
		if key == submission_id:
			return True
	return False


def gen_log(data):
	datetime =  str(time.strftime("%Y/%m/%d")) + " " + str(time.strftime("%H:%M:%S"))
	print datetime + ": " + data


### MAIN #############################################
r = praw.Reddit("/r/rainmeter source enforcer by /u/Pandemic21")
USERNAME=''
PASSWORD=''
GRACE_PERIOD=60*60*6 # 6 hours in seconds	
COMMENT_TEXT="It looks like your submission does not comply with Rule B.1.\n\n>If you share a completed setup, provide download links to skins and wallpapers shown within six hours of posting.\n\nPlease reply to your submission with the download links."
sub = r.get_subreddit("rainmeter")
d = {}

r.login(USERNAME,PASSWORD,disable_warning=True)

while 1:
	#search for new submissions
	posts = sub.get_new(limit=10)
	for post in posts:
		if post.is_self:
			gen_log(post.id + " is a self-post")
			continue
		if get_entry_exists(post.id):
			gen_log(post.id + " has already been added")
			continue
		gen_log("Adding " + post.id)
		d[post.id] = int(post.created_utc) + GRACE_PERIOD

	#check old submissions
	t = time.time()

	for key in d.keys():
		if float(d[key]) > t:
			gen_log(str(key) + " has " + str(int((d[key])-t)/60) + " minutes left")
			continue

		gen_log("Checking " + str(key) + "...")
		
		op_has_replied = False
		s = r.get_submission(submission_id=key)
		op = str(s.author)
		comments = s.comments

		for comment in comments:
			if op == str(comment.author):
				gen_log("OP replied, comment.id = " + comment.id)
				op_has_replied = True
		if op_has_replied:
			continue
		gen_log("OP hasn't replied, adding comment")
		s.add_comment(COMMENT_TEXT)
		#delete dictionary entry
		d.pop(key)

	time.sleep(60)
