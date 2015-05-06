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
