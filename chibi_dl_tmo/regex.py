import re


re_show = re.compile( r'https://(tmofans|lectortmo|visortmo|zonatmo).com/library/\w*/\d*/.*' )

re_follow = re.compile( r'https://(tmofans|lectortmo|visortmo|zonatmo).com/profile/follow' )
re_pending = re.compile( r'https://(tmofans|lectortmo|visortmo|zonatmo).com/profile/pending' )
re_read = re.compile( r'https://(tmofans|lectortmo|visortmo|zonatmo).com/profile/read' )
