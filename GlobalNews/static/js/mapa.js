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


              for(i=0; i<data.lista_noticias.length; i++){
                var marker1 = new google.maps.Marker({
                position: new google.maps.LatLng(data.lista_noticias[i].latitud,data.lista_noticias[i].longitud),
                map: map,
                title: data.lista_noticias[i].titulo,
                url: '/publicacion/' + data.lista_noticias[i].id
                });
                google.maps.event.addListener(marker1, 'click', function() {
                window.location.href = this.url;
                });

              }

              for(i=0; i<data.notas_result.length; i++){
                var marker1 = new google.maps.Marker({
                position: new google.maps.LatLng(data.notas_result[i].latitud,data.notas_result[i].longitud),
                map: map,
                icon: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                title: data.notas_result[i].titulo,
                url: '/publicacion/geolocalizacion/' + data.notas_result[i].id
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