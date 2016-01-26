
window.onload = function onload(){
  var cards = document.getElementsByClassName('js-makes-it');
  for (var card in cards) {
    cards[card].onclick = manageClickOnCard;
  }
};



function manageClickOnCard(evt) {
  var teamAbbr = evt.srcElement.dataset.team;
  fetch('/in_or_out.json?team=' + teamAbbr).then(function(response) {
    return response.json();
  }).then(function(results) {
    alert('Current Position is: ' + results.currentPosition);
  });
}