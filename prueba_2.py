#!/usr/bin/python
import json
import requests


# Función para la busqueda de ID y obtener valores de Measurments
def busqueda_id(values, searchId):
    for i in range(len(values)):
        valores = values[i]
        get_id = valores.get('_id')
        
        # Corroborar que el Id buscado está en los ids
        if get_id == searchId:
            stat = valores.get('stations')[0]
            meas = stat.get('measurements')[0]
            pollutant = meas.get('pollutant')
            value = meas.get('value')
            unit = meas.get('unit')

            Data = {'is_id':True, 'value':value, 'units':unit, 'pollutant':pollutant}
            break
        else:
            
            Data = {"is_id":False}

    return Data    

def last_id_pollulant(values, searchPoll):
    values.reverse()

    for i in range(len(values)):
        valores = values[i]
        get_id = valores.get('_id')
        stat = valores.get('stations')
        meas = stat[0]
        try:
            poll = meas.get('measurements')[0]
            pollutant = poll.get('pollutant')
            if pollutant == searchPoll:
                Data = {'_id':get_id, "pollutant":pollutant}
                break
        except:
            None
    return Data  

def ultimo_id(values, searchId):
    for i in range(len(values)):
        valores = values[i]
        get_id = valores.get('_id')
        
        # Corroborar que el Id buscado está en los ids
        if get_id == searchId:
            stat = valores.get('stations')[0]
            meas = stat.get('measurements')[0]
            pollutant_one = meas.get('pollutant')
            
            # Se invierte los valore de values
            values.reverse()

            for i in range(len(values)):
                valores = values[i]
                get_id = valores.get('_id')
                stat = valores.get('stations')
                meas = stat[0]
                try:
                    poll = meas.get('measurements')[0]
                    pollutant = poll.get('pollutant')
                    if pollutant == pollutant_one:
                        Data = {"is_id":True, '_id':get_id, "pollutant":pollutant}
                        break
                except:
                    None
            return Data
        else:
            
            Data = {"is_id":False}

    return Data  

# Recibir información de la API y convertirlo en un dict
response = requests.get('https://api.datos.gob.mx/v1/calidadAire')
json_data = response.json()

# Determinar id a buscar
id_busqueda = "58c780bf281e87010078f491"

# Extraemos la lista en los resultados
resultados = json_data['results']

# Se aplica la función y se guarda en una variable
busqueda = busqueda_id(resultados, id_busqueda)
print('Se encontró: el id: %s \n%s' % (id_busqueda, busqueda))

busqueda_last = last_id_pollulant(resultados, busqueda.get('pollutant'))
print('El último id que coincide con el pollutant es:\n%s' % busqueda_last)

print("\nEvent listener")

# Se define una clase para detectar cambios en data, y ejecutar las funciones
class get_pollutant(object):
    def __init__(self,data):
        self.data = data
        if self.data == True:
            self.last_id = ultimo_id(resultados, id_busqueda)
            print(self.last_id)
            if self.last_id.get('is_id') == True:
                self.do_again = busqueda_id(resultados, id_busqueda)
                print(self.do_again)


data = ""

if __name__ == '__main__':
    busqueda_pollutant = busqueda_id(resultados, id_busqueda)
    print(busqueda_pollutant)
    data = busqueda_pollutant.get('is_id')
    p = get_pollutant(data)