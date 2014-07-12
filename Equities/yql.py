import yahoo.yql

response = yahoo.yql.YQLQuery().execute('select * from delicious.feeds.popular')
if 'query' in response and 'results' in response['query']:
      print response['query']['results']
elif 'error' in response:
      print 'YQL query failed with error: "%s".' % response['error']['description']
else:
      print 'YQL response malformed.'
