var http = require('http');
var server = http.createServer().listen(3000);
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');
var redis = require('redis');

var sub = redis.createClient();

var host = 'localhost';
var usuarios = [];

var callback = function(channel, message){
    var datos = JSON.parse(message);
    switch (channel) {
        case 'chat':

            io.to('chat_' + datos.id_chat ).emit('mensaje_entrada', datos);
            break;

        case 'publicacion':
            io.sockets.emit('nueva_publicacion', datos);
            break;
    }
};
//Se subscribe al canal de chat
sub.subscribe('chat');
sub.subscribe('publicacion');
sub.addListener('message', callback);

io.sockets.on('connection', function (socket) {

    //Configure socket.io to store cookie set by Django
    io.set('authorization', function(data, accept){
        if(data.headers.cookie){
            data.cookie = cookie_reader.parse(data.headers.cookie);
            return accept(null, true);
        }
        return accept('error', false);
    });
    io.set('log level', 1);

    var contador = 0;

    //Usuario conectado
    console.log('Conectado');

    //Arreglo para guardar ids del usuario
    var session_id = socket.handshake.headers.cookie.slice(-32);
    obj_usuario = {
        'session_id': session_id,
        'socket_id': socket.id
    };

    //Arir chat
    socket.on('abrir_chat', function(id_chat){
        canal_chat = 'chat_' + id_chat;
        console.log('Unido a ' + canal_chat);
        socket.join(canal_chat);
    });

    //Nuevo mensaje en el chat
    socket.on('nuevo_mensaje_chat', function(data){

        valores = querystring.stringify(data);

        var options = {
            host: 'localhost',
            port: 8000,
            path: '/nuevo/mensaje/',
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': valores.length
            }
        };        

        //Enviar mensaje a Django
        var req = http.get(options, function(res){
            res.setEncoding('utf8');

        });
        
        req.write(valores);
        req.end();
    });

    // Unsubscribe after a disconnect event
    socket.on('disconnect', function () {
        console.log('Ya me fui');
    });
});