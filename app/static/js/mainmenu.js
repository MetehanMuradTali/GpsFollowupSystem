var map
        let markers = []
        const users_cars=document.getElementsByClassName("users_cars")
        const hold = document.getElementById("hold")
        const hold2 = document.getElementById("hold2")
        const btn = document.getElementById("Search")
        const firstdate = document.getElementById("firstdate")
        const seconddate =  document.getElementById("seconddate")

        var socket = io.connect("http://127.0.0.1:5000/");
        socket.on('connect', function() {
            console.log("Bağlanıldı")
        });
        socket.on('Connected', function(gelen_veri) {
            console.log(gelen_veri)
        });
        btn.addEventListener('click',function(event){
           socket.emit("Request",{'firstdate':firstdate.value,'seconddate':seconddate.value,'car_id':hold.innerHTML})
        });
        for(var i=0;i<users_cars.length;i++){
             users_cars[i].addEventListener('click',function (){
                 hold.innerHTML=this.id
                 socket.emit('ReqLastCoordinate',this.id)
            })
        }
        socket.on('SendLastCoordinate',function (gelen_veri){
            gelen_veri[0]['Date']=gelen_veri[0]['Date'].replace(" ","T")
            firstdate.value = (gelen_veri[0]['Date'])
            seconddate.value=firstdate.value
            seconddate.stepDown(30)
        })

        document.addEventListener("DOMContentLoaded",loadDatasToMap());

        function loadDatasToMap(){
            socket.emit('RequestLoad')
        }

        function initMap() {
             const center = new google.maps.LatLng(59.334591,18.063240)
             var options = {
                 zoom:7,
                 center:center
             }
            map = new google.maps.Map(document.getElementById('map'),options)

            socket.on('Answer', function(gelen_veri) {
                setMapOnAll(null);
                markers = [];
                addMarkersToArray(gelen_veri)
                setMapOnAll(map)
            });
             socket.on('Answers', function(gelen_veri) {
                setMapOnAll(null);
                markers = [];
                addMarkersToArray(gelen_veri["query1"])
                addMarkersToArray(gelen_veri["query2"])
                setMapOnAll(map)

            });
            socket.on('Load', function(gelen_veri) {
                gelen_veri["query1"][0]['Date']=gelen_veri["query1"][0]['Date'].replace(" ","T")
                firstdatetime=gelen_veri["query1"][0]['Date']
                hold2.value=firstdatetime
                hold2.stepDown(30)
                seconddatetime=hold2.value
                car_id=gelen_veri["query1"][0]['Id']
                //
                //
                gelen_veri["query2"][0]['Date']=gelen_veri["query2"][0]['Date'].replace(" ","T")
                firstdatetime2=gelen_veri["query2"][0]['Date']
                hold2.value=firstdatetime2
                hold2.stepDown(30)
                seconddatetime2=hold2.value
                car_id2=gelen_veri["query2"][0]['Id']
                socket.emit("Requests",{'firstdate1':firstdatetime,'seconddate1':seconddatetime,'car_id1':car_id,
                    'firstdate2':firstdatetime2,'seconddate2':seconddatetime2,'car_id2':car_id2})
            });

        }
        function setMapOnAll(map) {
          for (let i = 0; i < markers.length; i++) {
            markers[i].setMap(map);
          }
        }
        function addMarkersToArray(gelen_veri){
            var icons = ["http://maps.google.com/mapfiles/ms/icons/yellow.png",
                "http://maps.google.com/mapfiles/ms/icons/blue.png",
                "http://maps.google.com/mapfiles/ms/icons/red.png",
                "http://maps.google.com/mapfiles/ms/icons/green.png",
                "http://maps.google.com/mapfiles/ms/icons/purple.png",
                "http://maps.google.com/mapfiles/ms/icons/lightblue.png",
                "http://maps.google.com/mapfiles/ms/icons/orange.png",
                "http://maps.google.com/mapfiles/ms/icons/pink.png",

            ];
            var colournumber =Math.floor(Math.random()*icons .length)
            for(i=0;i<gelen_veri.length;i++){
                var marker = new google.maps.Marker({
                    position:new google.maps.LatLng(parseFloat(gelen_veri[i]['Nat']),parseFloat(gelen_veri[i]['Lang'])),
                    icon:icons[colournumber],
                })
               markers.push(marker);}
        }