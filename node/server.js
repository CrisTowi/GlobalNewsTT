//Importar los módulos
var http = require('http');
var server = http.createServer().listen(3000);
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');
var MongoClient = require('mongodb').MongoClient;

var host = 'localhost';
var usuarios = [];

//Crear un cliente Redis
var redis = require('redis');
var sub = redis.createClient();

//Funcion que maneja cada evento enviado desde Django
var recibeMensaje = function(channel, message){
    var i,j;
    var datos = JSON.parse(message);
    switch (channel) {
        case 'chat':
            io.to('chat_' + datos.id_chat ).emit('mensaje_entrada', datos);
            break;

        case 'publicacion':

            for(j=0; j<datos.lista_usuarios.length; j++){            
                for(i=0; i<usuarios.length; i++){
                    if(usuarios[i].session_id == datos.lista_usuarios[j]){
                        io.to(usuarios[i].socket_id).emit('nueva_publicacion', datos);
                    }
                }
            }
            break;

        case 'comentario':
            for(i=0; i<usuarios.length; i++){
                if(usuarios[i].session_id == datos.session_key){
                    io.to(usuarios[i].socket_id).emit('nuevo_comentario', datos);
                }
            }
            break;

        case 'me_gusta':
            for(i=0; i<usuarios.length; i++){
                if(usuarios[i].session_id == datos.session_key){
                    io.to(usuarios[i].socket_id).emit('me_gusta', datos);
                }
            }
            break;

        case 'nuevo_seguidor':
            for(i=0; i<usuarios.length; i++){
                if(usuarios[i].session_id == datos.session_key){
                    io.to(usuarios[i].socket_id).emit('nuevo_seguidor', datos);
                }
            }
            break;
    }
};

//Subscribe a los diferentes canales
sub.subscribe('chat');
sub.subscribe('publicacion');
sub.subscribe('comentario');
sub.subscribe('nuevo_seguidor');
sub.subscribe('me_gusta');

//Evento que recibe mensaje de redis
sub.addListener('message', recibeMensaje);

io.sockets.on('connection', function (socket) {
MongoClient.connect('mongodb://localhost:27017/globalnews', function(err, db) {
    if(err) throw err;
    //Usuario conectado
    index_sessionid = socket.handshake.headers.cookie.indexOf('sessionid=');

    //Arreglo para guardar ids del usuario
    var session_id = socket.handshake.headers.cookie.slice(index_sessionid + 10, index_sessionid + 10 +32);

    //var session_id = socket.handshake.headers.cookie.slice(-32);
    obj_usuario = {
        'session_id': session_id,
        'socket_id': socket.id,
        coords: {
            lat: socket.handshake.query.lat,
            lon: socket.handshake.query.lon
        }
    };

    usuarios.push(obj_usuario);
        var doc = {
            '_id': obj_usuario.socket_id,
            "loc" : {
                "type" : "Point",
                "coordinates" : [
                Number(obj_usuario.coords.lon),
                Number(obj_usuario.coords.lat)
                ]
            }
        }
        db.collection('usuarios').insert(doc, function(err, inserted) {
            if(err) throw err;
        });

    //COnfigurar las cookies para comunicarse con Django
    io.set('authorization', function(data, accept){
        if(data.headers.cookie){
            data.cookie = cookie_reader.parse(data.headers.cookie);
            return accept(null, true);
        }
        return accept('error', false);
    });

    //Arir chat
    socket.on('abrir_chat', function(id_chat){
        console.log('Abrio el chat');
        console.log(id_chat);
        canal_chat = 'chat_' + id_chat;
        socket.join(canal_chat);
    });

    //Nuevo mensaje en el chat
    socket.on('nuevo_mensaje_chat', function(data){

        valores = querystring.stringify(data);

        var options = {
            host: host,
            port: 8000,
            path: '/nuevo/mensaje/',
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': valores.length
            }
        };        

        //Enviar mensaje a Django y termina el request
        var req = http.get(options, function(res){
            res.setEncoding('utf8');
        });
        req.write(valores);
        req.end();
    });

    // Desconectar al usuario y sacarlo de la lista de usuarios
    socket.on('disconnect', function (socket) {
        for(var i=0; i<usuarios.length; i++){
            if(usuarios[i].socket_id == this.id){
                usuarios.splice(i, 1);
            }
        }
        console.log(this.id);
        db.collection('usuarios').remove({"_id": String(this.id)}, function(err, removed) {
            if(err) throw err;
        });
    });
});
});