var host = "localhost";



if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position){
        lat = position.coords.latitude;
        lon = position.coords.longitude;

        parameters = {
          lat: lat,
          lon: lon
        }
        var socket = io.connect(host + ":3000", {query:parameters});
        //Cuando llegue un nuevo mensaje
        socket.on('nuevo_comentario', function(data){
            var n = noty({
                text: '<span class="texto_noty" data-id_nota="' + data.nota_id + '"> Nuevo Comentario: <br>' + data.contenido + ' de ' + data.usuario + '<br> en ' + data.nota + '</span>',
                layout: 'bottomRight',
                type: 'information',
                timeout: 3500,
                animation: {
                    open: {height: 'toggle'}, // jQuery animate function property object
                    close: {height: 'toggle'}, // jQuery animate function property object
                    easing: 'swing', // easing
                    speed: 500 // opening & closing animation speed
                }
            });
            $('.texto_noty').on('click', function(){
                window.location.href = '/publicacion/' + $(this).data('id_nota');
            });
        });

        socket.on('me_gusta', function(data){
            var n = noty({
                text: '<span class="texto_noty" data-id_nota="' + data.nota_id + '"> A: ' + data.usuario + ' le gusta ' + data.nota + '</span>',
                layout: 'bottomRight',
                type: 'information',
                timeout: 3500,
                animation: {
                    open: {height: 'toggle'}, // jQuery animate function property object
                    close: {height: 'toggle'}, // jQuery animate function property object
                    easing: 'swing', // easing
                    speed: 500 // opening & closing animation speed
                }
            });
            $('.texto_noty').on('click', function(){
                window.location.href = '/publicacion/' + $(this).data('id_nota');
            });
        });

        socket.on('nuevo_seguidor', function(data){
            var n = noty({
                text: '<span class="texto_noty_seguidor" data-id_usuario="' + data.seguidor_id + '">¡Nuevo seguidor! <br>' + data.seguidor + ' te ha seguido </span>',
                layout: 'bottomRight',
                type: 'success',
                timeout: 3500,
                callback: { onClose: function() { /* Go to the URL i want to go */ }},
                animation: {
                    open: {height: 'toggle'}, // jQuery animate function property object
                    close: {height: 'toggle'}, // jQuery animate function property object
                    easing: 'swing', // easing
                    speed: 500 // opening & closing animation speed
                }
            });
            $('.texto_noty_seguidor').on('click', function(){
                window.location.href = '/perfil/' + $(this).data('id_usuario');
            });
        });
        var left_right = 1;
        
        socket.on('nueva_publicacion', function(data){

            var ubicacion = '';

            if(left_right == 1){
                ubicacion = ' class="timeline-inverted"';
                left_right = 0;
            } else {
                ubicacion = '';
                left_right = 1;
            }

            var template = $('<li' + ubicacion + '> \
                                        <div class="timeline-badge"><i class="fa fa-check"></i> \
                                        </div> \
                                        <div class="timeline-panel"> \
                                            <div class="timeline-heading"> \
                                                <a href="/publicacion/' + data.id + '"><h4 class="timeline-title">' + data.titulo + '</h4></a> \
                                                <a href="/perfil/' + data.usuario_id + '"><h5>Por ' + data.usuario + '</h5></a> \
                                                <p> \
                                                    <small class="text-muted"><i class="fa fa-time"></i>' + data.fecha + '</small> \
                                                </p> \
                                            </div> \
                                            <div class="timeline-body"> \
                                                <p>' + data.descripcion + '</p> \
                                            </div> \
                                        </div> \
                                    </li>');
            template.hide();
            $('#timeline').prepend(template);
            template.show('slow');


            var marker1 = new google.maps.Marker({
                position: new google.maps.LatLng(data.latitud,data.longitud),
                map: map,
                title: data.titulo,
                url: '/publicacion/' + data.id
                });
                google.maps.event.addListener(marker1, 'click', function() {
                window.location.href = this.url;
            });
            var n = noty({
                text: '<span class="texto_noty" data-id_nota="' + data.id + '"> Una noticia que te puede interesar </span>',
                layout: 'bottomRight',
                type: 'information',
                timeout: 3500,
                animation: {
                    open: {height: 'toggle'}, // jQuery animate function property object
                    close: {height: 'toggle'}, // jQuery animate function property object
                    easing: 'swing', // easing
                    speed: 500 // opening & closing animation speed
                }
            });
            $('.texto_noty').on('click', function(){
                window.location.href = '/publicacion/' + $(this).data('id_nota');
            });
        });
        socket.on('nueva_publicacion_localizacion', function(data){

            var ubicacion = '';

            if(left_right == 1){
                ubicacion = ' class="timeline-inverted"';
                left_right = 0;
            } else {
                ubicacion = '';
                left_right = 1;
            }

            var template = $('<li' + ubicacion + '> \
                                        <div class="timeline-badge"><i class="fa fa-check"></i> \
                                        </div> \
                                        <div class="timeline-panel"> \
                                            <div class="timeline-heading"> \
                                                <a href="/publicacion/' + data.id + '"><h4 class="timeline-title">' + data.titulo + '</h4></a> \
                                                <a href="/perfil/' + data.usuario_id + '"><h5>Por ' + data.usuario + '</h5></a> \
                                                <p> \
                                                    <small class="text-muted"><i class="fa fa-time"></i>' + data.fecha + '</small> \
                                                </p> \
                                            </div> \
                                            <div class="timeline-body"> \
                                                <p>' + data.descripcion + '</p> \
                                            </div> \
                                        </div> \
                                    </li>');
            template.hide();
            $('#timeline').prepend(template);
            template.show('slow');


            var marker1 = new google.maps.Marker({
                position: new google.maps.LatLng(data.latitud,data.longitud),
                map: map,
                title: data.titulo,
                url: '/publicacion/' + data.id
                });
                google.maps.event.addListener(marker1, 'click', function() {
                window.location.href = this.url;
            });
            var n = noty({
                text: '<span class="texto_noty" data-id_nota="' + data.id + '"> Una nueva noticia cercana a ti </span>',
                layout: 'bottomRight',
                type: 'information',
                timeout: 3500,
                animation: {
                    open: {height: 'toggle'}, // jQuery animate function property object
                    close: {height: 'toggle'}, // jQuery animate function property object
                    easing: 'swing', // easing
                    speed: 500 // opening & closing animation speed
                }
            });
            $('.texto_noty').on('click', function(){
                window.location.href = '/publicacion/' + $(this).data('id_nota');
            });

        });
    });
}

