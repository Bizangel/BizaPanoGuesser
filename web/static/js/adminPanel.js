var socket = io('/admin');

const AdminToken = document.getElementById('tokenHolder').getAttribute('token')

document.getElementById('debugButton').addEventListener('click',(e)=>{
    socket.emit('admin-debug',{pwd: AdminToken})
})

document.getElementById('pano-enqueue-button').addEventListener('click',(e)=>{
    socket.emit('admin-pano-enqueue',{pwd: AdminToken})
})


document.getElementById('startGame').addEventListener('click',(e)=>{
    var totalrounds = document.getElementById("totalrounds").value
    var roundduration = document.getElementById("roundduration").value
    socket.emit('admin-startGame',{pwd: AdminToken,
        totalrounds: totalrounds, round_duration: roundduration})
})


document.getElementById('setPanoParams').addEventListener('click',(e)=>{
    var urban = document.getElementById("urban").checked
    var indoors = document.getElementById("indoors").checked
    var countryNumber = document.getElementById("countryNumber").value

    if (!countryNumber){
        countryNumber = null;
    }

    socket.emit('admin-setPanoParams', {pwd: AdminToken, urban :  urban,
    indoors: indoors, countryNumber: countryNumber})
})

socket.on('message',(mess) =>{
    document.getElementById("messageholder").innerHTML = mess
})
