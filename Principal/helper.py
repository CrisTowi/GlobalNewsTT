import pymongo

client = pymongo.MongoClient()

def guardar_nota(nota):
	notas = client.globalnews.notas

	titulo = nota.titulo
	_id = nota.id
	lat = float(nota.latitud)
	lng = float(nota.longitud)

	notas.insert({'_id': _id, 'titulo': titulo, 'loc': {'type': 'Point', 'coordinates': [lng, lat]}})

def obtener_notas_loc(lng, lat, notas):
	notas_result = []
	result = pymongo.MongoClient().globalnews.command(
	    'geoNear', 'notas',
		near={
		    'type': 'Point',
		    'coordinates': [
		        float(lng),
		        float(lat)]},
		maxDistance= 7000,
		spherical=True,
		num=10)

	for resultado in result['results']:
		for nota in notas:
			if (resultado['obj']['_id'] == nota['id']):
				notas_result.append(nota)

	print(notas_result)
	return notas_result
