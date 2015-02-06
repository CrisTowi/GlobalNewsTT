var map = null;
function initialize(){
    var lat, lon;
    
    $.get('/puntos', function(data){

      if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position){
              lat = position.coords.latitude;
              lon = position.coords.longitude;
                  var mapProp = {

            center:new google.maps.LatLng(lat,lon),
            zoom:13,
            mapTypeId:google.maps.MapTypeId.ROADMAP
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

        });
      }

    });
}

google.maps.event.addDomListener(window, 'load', initialize);