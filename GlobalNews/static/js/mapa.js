var map = null;
function initialize(){
    var lat, lon;
    var im = 'http://www.robotwoods.com/dev/misc/bluecircle.png';
    
      if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position){
            lat = position.coords.latitude;
            lon = position.coords.longitude;

            parameters = {
              lat: lat,
              lon: lon
            }

            $.get('/puntos', parameters ,function(data){
            var mapProp = {
              center:new google.maps.LatLng(lat,lon),
              zoom:13,
              mapTypeId:google.maps.MapTypeId.ROADMAP,
              disableDefaultUI: true
            };
              map=new google.maps.Map(document.getElementById("googleMap")
            ,mapProp);


              for(i=0; i<data.length; i++){
                var marker1 = new google.maps.Marker({
                position: new google.maps.LatLng(data[i].latitud,data[i].longitud),
                map: map,
                title: data[i].titulo,
                url: '/publicacion/' + data[i].id
                });
                google.maps.event.addListener(marker1, 'click', function() {
                window.location.href = this.url;
                });

              }

            var userMarker = new google.maps.Marker({
              position: new google.maps.LatLng(lat,lon),
              map: map,
              title: 'Mi Ubicación',
              icon: im
            });
          });
        });
      }

}

google.maps.event.addDomListener(window, 'load', initialize);