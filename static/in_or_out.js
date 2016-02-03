
window.onload = function onload() {
    var cards = document.getElementsByClassName('js-makes-it');
    for (var card in cards) {
        cards[card].onclick = manageClickOnCard;
    }
};

function manageClickOnCard(evt) {
    evt.stopPropagation();
    evt.returnValue = false;

    var teamAbbr = evt.srcElement.dataset.team;
    fetch('/in_or_out.json?team=' + teamAbbr).then(function(response) {
        return response.json();
    }).then(function(results) {
        if (results.error) {
            alert(results.error);
        } else {
            alert(JSON.stringify(results));
        }
    });
}

var chart;
var chartData = [];

function reCalcChartData() {
    chartData = [];

    dataForTeams(['SAC', 'UTA', 'HOU', 'POR', 'CLE'], {'algo': 'pos-based'}, function(response) {
        teams = createChartDataFromResponse(response);
        drawChartData(teams);
    });
}

function drawChartData(teams) {
    var chartConfiguration = {
        'type': 'serial',
        'theme': 'chalk',
        'legend': {
            'useGraphSettings': true
        },
        'dataProvider': chartData,
        'valueAxes': [{
            'id': 'v1',
            'axisColor': '#FF6600',
            'axisThickness': 2,
            'gridAlpha': 0,
            'axisAlpha': 1,
            'position': 'left'
        }],
        'graphs': [],
        'chartScrollbar': {},
        'chartCursor': {
            'cursorPosition': 'mouse'
        },
        'categoryField': 'date',
        'categoryAxis': {
            'parseDates': true,
            'axisColor': '#DADADA',
            'minorGridEnabled': true
        }
    };
    for (var i = 0; i < teams.length; i++) {
        chartConfiguration.graphs.push({
            'valueAxis': 'v1',
            'lineColor': ['#FF6600', '#FCD202', '#B0DE09', '#DADADA', '#77B6E0'][i % 5],
            'bullet': ['round', 'square', 'triangleUp', 'triangleDown', 'bubble'][i % 5],
            'balloonText': ['[[name_', i, ']] vs <b>[[vs_whom_', i, ']]</b>'].join(''),
            'bulletBorderThickness': 1,
            'hideBulletsCount': 0,
            'title': teams[i],
            'valueField': 'wins_for_' + i,
            'fillAlphas': 0
        });
    };

    chart = AmCharts.makeChart('chartdiv', chartConfiguration);

    // WRITE
    chart.write('chartdiv');
}

function createChartDataFromResponse(response) {
    var count = 0;
    var names = [];
    var dates = [];
    Object.keys(response).forEach(function(key) {
        data_for_key = response[key];
        var stats = data_for_key.stats.split('|');
        var game_dates = data_for_key.game_dates.split('|');
        var vs_whom = data_for_key.vs_whom.split('|');
        var game_dates_as_int = data_for_key.game_dates_as_int.split('|');
        for (var i = 0; i < stats.length; i++) {
            var dataPoint = {};
            dataPoint['game_date_as_int'] = game_dates_as_int[i];
            dataPoint['vs_whom_' + count] =  vs_whom[i];
            dataPoint['name_' + count] = data_for_key.name;
            eval('dataPoint["wins_for_' + count + '"]=' + stats[i]);

            if (dates[game_dates[i]]) {
                dates[game_dates[i]] = Object.extend(dates[game_dates[i]], dataPoint);
            } else {
                dates[game_dates[i]] = dataPoint;
            }
        }
        count++;
        names.push(data_for_key.name);
    });

    for (var date in dates) {
        var entry = dates[date];
        entry.date = new Date(date);
        chartData.push(entry);
    }

    chartData.sort(function(game0, game1) {
        var x = parseInt(game0.game_date_as_int, 10);
        var y = parseInt(game1.game_date_as_int, 10);
        if (x < y) {return -1; }
        if (x > y) {return 1; }
        return 0;
    });

    return names;
}

function dataForTeams(teamsArr, options, callback) {
    fetch('/upcoming_games_for_teams.json?teams=' + teamsArr.join(',')).then(function(response) {
        return response.json();
    }).then(function(results) {
        if (results.error) {
            alert(results.error);
        } else {
            callback(results);
        }
    });

}

Object.extend = function(destination, source) {
    for (var property in source) {
        if (source.hasOwnProperty(property)) {
            destination[property] = source[property];
        }
    }
    return destination;
};

