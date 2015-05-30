var host = "localhost";

if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position){
        lat = position.coords.latitude;
        lon = position.coords.longitude;
        var left_right = 1;

        parameters = {
          lat: lat,
          lon: lon
        }
        var socket = io.connect(host + ":3000", {query:parameters});

        $('.btn-abre-platica').on('click', function(e){
            e.preventDefault();
            var alerta = $('#alerta-mensaje');
            alerta.hide();

            $("#btn-enviar").off('click');
            $('#chat').html("");

            var id_usuario = $(this).data("usuario");
            var username_chat = $(this).data("username");
            var imagen = $(this).data("imagen");
            var username_local =  $(this).data("user");
            var usuario = $('#input_usuario').val();
            var media_url = $('#media_url').val();
            var imagen_local = $(this).data("userfoto");
            var id_chat = "";

            $('#nombre-usuario-chat').html(username_chat);
            var id_chat = $(this).data("chat");

            $.get( "/get/chat/" + id_usuario, function(data){
                id_chat = data.id;
                socket.emit('abrir_chat', id_chat);
            });


            var mensaje_entrada = function(objeto){
               var imagen_url = media_url + imagen_local
                        if(objeto.usuario_remitente == id_usuario){ 
                var imagen_url = media_url + imagen;
                var template = $('<li class="left clearfix"> \
                                    <span class="chat-img pull-left"> \
                                        <img src=" ' + imagen_url + ' " alt="User Avatar" width="50px" class="img-circle" /> \
                                    </span> \
                                    <div class="chat-body clearfix"> \
                                        <div class="header"> \
                                            <strong class="primary-font">' + username_chat + '</strong> \
                                            <small class="pull-right text-muted"> \
                                                <i class="fa fa-clock-o fa-fw"></i> ' + objeto.fecha + ' \
                                            </small> \
                                        </div> \
                                        <p> \
                                            ' + objeto.contenido + ' \
                                        </p> \
                                    </div> \
                                </li>');
                        } else {
                var imagen_url = media_url + imagen_local
                var template = $('<li class="right clearfix"> \
                                    <span class="chat-img pull-right"> \
                                        <img src="' + imagen_url + '" alt="User Avatar" width="50px" class="img-circle" /> \
                                    </span> \
                                    <div class="chat-body clearfix"> \
                                        <div class="header"> \
                                            <small class=" text-muted"> \
                                                <i class="fa fa-clock-o fa-fw"></i>' + objeto.fecha + '</small> \
                                            <strong class="pull-right primary-font">' + username_local + '</strong> \
                                        </div> \
                                        <p> \
                                            '+ objeto.contenido +' \
                                        </p> \
                                        <a href="#" class="eliminar" data-id="' + objeto.id + '">Eliminar</a> \
                                    </div> \
                                </li>');
                        }



                   template.hide();
                   $('#chat').append(template);
                   template.show('slow');


                   $('#mensaje').val('');      
            }

            socket.addEventListener('mensaje_entrada', mensaje_entrada);


            $('#ModalMD').on('hidden.bs.modal', function () {
                socket.removeEventListener('mensaje_entrada', mensaje_entrada);
            });

            obtenerChat(id_usuario, username_chat, imagen, username_local, usuario, media_url, imagen_local);
            $('#btn-enviar').on('click', function(){
                var mensaje = $('#mensaje').val();
                if (mensaje == '') {
                  alerta.fadeIn('slow');
                  setTimeout(function() {
                    alerta.fadeOut('slow');
                  }, 3000);
                } else {
                  var info = {usuario_consultor: usuario , usuario_chat: id_usuario, mensaje: mensaje, id_chat: id_chat};
                  socket.emit('nuevo_mensaje_chat', info);
                }
            });

            $(document).on("click", ".eliminar", function(){
              event.preventDefault();
              var id = $(this).data("id");
                $.get( "/eliminar/mensaje/", {id: id}, function(data){
                  $('#chat').html("");
                  var n = noty({
                      text: 'Mensaje eliminado con éxico',
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
                  $(document).unbind("click", ".eliminar");
                  obtenerChat(id_usuario, username_chat, imagen, username_local, usuario, media_url, imagen_local);
                });
            });
        });

        function obtenerChat(id_usuario, username_chat, imagen, username_local, usuario, media_url, imagen_local){
        $.ajax({
                  url: "/chat/",
                  type: "GET", //send it through get method
                  data: {usuario_consultor: usuario , usuario_chat: id_usuario},
                  success: function(response) {
            
                    $.each(response, function(i, objeto){



                        if(objeto.usuario_remitente_id == id_usuario){ 
                var imagen_url = media_url + imagen;
                var template = '<li class="left clearfix"> \
                                    <span class="chat-img pull-left"> \
                                        <img src=" ' + imagen_url + ' " alt="User Avatar" width="50px" class="img-circle" /> \
                                    </span> \
                                    <div class="chat-body clearfix"> \
                                        <div class="header"> \
                                            <strong class="primary-font">' + username_chat + '</strong> \
                                            <small class="pull-right text-muted"> \
                                                <i class="fa fa-clock-o fa-fw"></i> ' + objeto.fecha + ' \
                                            </small> \
                                        </div> \
                                        <p> \
                                            ' + objeto.contenido + ' \
                                        </p> \
                                    </div> \
                                </li>';
                        } else {
                var imagen_url = media_url + imagen_local
                var template = '<li class="right clearfix"> \
                                    <span class="chat-img pull-right"> \
                                        <img src="' + imagen_url + '" alt="User Avatar" width="50px" class="img-circle" /> \
                                    </span> \
                                    <div class="chat-body clearfix"> \
                                        <div class="header"> \
                                            <small class=" text-muted"> \
                                                <i class="fa fa-clock-o fa-fw"></i>' + objeto.fecha + '</small> \
                                            <strong class="pull-right primary-font">' + username_local + '</strong> \
                                        </div> \
                                        <p> \
                                            '+ objeto.contenido +' \
                                        </p> \
                                        <a href="#" class="eliminar" data-id="' + objeto.id + '">Eliminar</a> \
                                    </div> \
                                </li>';
                        }
                    $('#chat').prepend(template);
                });
              }
        });
        }


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
        

        socket.on('usuario_reportado', function(data){
            var n = noty({
                text: '<span class="texto_noty_reportado">Has sido reportado varias veces. Revisa tu contenido </span>',
                layout: 'bottomRight',
                type: 'error',
                timeout: 3500,
                callback: { onClose: function() { /* Go to the URL i want to go */ }},
                animation: {
                    open: {height: 'toggle'}, // jQuery animate function property object
                    close: {height: 'toggle'}, // jQuery animate function property object
                    easing: 'swing', // easing
                    speed: 500 // opening & closing animation speed
                }
            });
            $('.texto_noty_reportado').on('click', function(){
                window.location.href = '/lista/notificaciones'
            });
        });

        socket.on('nota_reportada', function(data){
            var n = noty({
                text: '<span class="texto_noty_reportado">La nota '+ data.nota +' sido reportado varias veces. Revisa tu contenido </span>',
                layout: 'bottomRight',
                type: 'error',
                timeout: 3500,
                callback: { onClose: function() { /* Go to the URL i want to go */ }},
                animation: {
                    open: {height: 'toggle'}, // jQuery animate function property object
                    close: {height: 'toggle'}, // jQuery animate function property object
                    easing: 'swing', // easing
                    speed: 500 // opening & closing animation speed
                }
            });
            $('.texto_noty_reportado').on('click', function(){
                window.location.href = '/publicacion/' + nota_id
            });
        });        
        
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
            if (google != undefined) {
                var marker1 = new google.maps.Marker({
                    position: new google.maps.LatLng(data.latitud,data.longitud),
                    map: map,
                    title: data.titulo,
                    url: '/publicacion/' + data.id
                    });
                    google.maps.event.addListener(marker1, 'click', function() {
                    window.location.href = this.url;
                });
            }
        });
        socket.on('nueva_publicacion_localizacion', function(data){

            var ubicacion = '';
            console.log('Nueva publicacion geolocalizacion')

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
                window.location.href = '/publicacion/geolocalizacion/' + $(this).data('id_nota');
            });
            if (google != undefined) {            
                var marker1 = new google.maps.Marker({
                    position: new google.maps.LatLng(data.latitud,data.longitud),
                    map: map,
                    icon: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                    title: data.titulo,
                    url: '/publicacion/geolocalizacion/' + data.id + '?dis=' + (data.dis.toFixed(2))
                    });
                    google.maps.event.addListener(marker1, 'click', function() {
                    window.location.href = this.url;
                });
            }
        });
    });
}

