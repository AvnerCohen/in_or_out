
window.onload = function onload(){
  var cards = document.getElementsByClassName('js-makes-it');
  for (var card in cards) {
    cards[card].onclick = manageClickOnCard;
  }
};


function manageClickOnCard(evt) {
  evt.stopPropagation();
  var teamAbbr = evt.srcElement.dataset.team;
  fetch('/in_or_out.json?team=' + teamAbbr).then(function(response) {
    return response.json();
  }).then(function(results) {
    if (results.error) { 
      alert(results.error);
    } else {
      alert('Current Position is: ' + results.currentPosition);
    }
  });
}

