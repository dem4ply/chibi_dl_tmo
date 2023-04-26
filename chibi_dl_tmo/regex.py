import re


re_show = re.compile( r'https://(tmofans|lectortmo).com/library/\w*/\d*/.*' )

re_follow = re.compile( r'https://tmofans.com/profile/follow' )
re_pending = re.compile( r'https://tmofans.com/profile/pending' )
re_read = re.compile( r'https://tmofans.com/profile/read' )
