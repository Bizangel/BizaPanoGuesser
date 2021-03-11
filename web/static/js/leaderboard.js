


function displayLeaderboardAnimation(){
    var leader = document.getElementById('leaderboard-container')
    var pano = document.getElementById('panorama')

    document.getElementById('leaderboard-container').style.display = 'block'

    // var total = 100;
    // var CountDownInterval = setInterval(function() {
    //
    //     pano.style.height = total + 'vh';
    //     leader.style.height = (100 - total) + 'vh';
    //
    //     total -= 5;
    //
    //     if (total <= 0){
    //         clearInterval(CountDownInterval);
    //         pano.style.height = '100vh';
    //         leader.style.height = '100vh';
    //         displayScoreboard()
    //     }
    //
    // }, 20);

    leader.style.position = 'fixed'
    pano.style.position = 'fixed'
    leader.style.top = '-100vh'

    var total = 0;
    var CountDownInterval = setInterval(function() {

        pano.style.top = total + 'vh';
        leader.style.top = (-100 + total) + 'vh';

        total += 1;

        if (total >= 100){
            clearInterval(CountDownInterval);
            pano.style.top = ''
            pano.style.position = ''
            leader.style.top = ''
            leader.style.position = ''
            displayScoreboard()
        }

    }, 20);
}

// Receives a resultjson mapped like: {first: ['jug': 300], second: ['le jug': 200], third: ['le godjug', 100]}

// updateResults(resultjson){
//     document.querySelector('firstname').innerHTML =
//     document.querySelector('secondname').innerHTML =
//     document.querySelector('thirdname').innerHTML =
// }

// function panoLeaderSwitch(){
//     document.getElementById('panorama')
//     document.getElementById('')
// }
// if (red*0.299 + green*0.587 + blue*0.114) > 186 use #000000 else use #ffffff
