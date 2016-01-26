import httplib2
import json

base_team_data_request = 'http://stats.nba.com/stats/teaminfocommon?LeagueID=00&SeasonType=Regular%20Season&Season=2015-16&TeamId='
h = httplib2.Http()


def query_api(team_id):
    request_url = base_team_data_request + str(team_id)
    (resp_headers, content) = h.request(request_url, 'GET')
    if resp_headers['status'] != '200':
        print request_url
        print resp_headers
        print content

    return json.loads(content)


def position_from_results(common_info):
    ## Doom to break, but test for now
    print common_info['resultSets']
    position = common_info['resultSets'][0]['rowSet'][0][8]
    return position
