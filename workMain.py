import sys
from random import randint
from PyQt4 import QtCore, QtGui, uic
from couchdb.mapping import Document, TextField, IntegerField, Mapping
from couchdb.mapping import DictField, ViewField, BooleanField, ListField
from couchdb import Server
import couchdb
import datetime
import math
import decimal

class Ui_MainWindow(QtGui.QMainWindow):
    
    listaJugadores = []
    jugadoresAgregados = []

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("mainWtabs.ui", self)
        self.boton_confirmar.clicked.connect(self.recuperarPersona)
        #Accion para el boton del administrador que habilita tabs 
        self.boton_login.clicked.connect(self.autenticar)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.recuperarJugadores.clicked.connect(self.listarJugadores)
        self.boton_agregar__jug_equipo.clicked.connect(self.transferirJugadores)
        self.boton_equipo_aceptar.clicked.connect(self.insertarEquipo)
        self.botonAgregarEquipo.clicked.connect(self.agregarListaEquipo)
        self.botonEliminarEquipo.clicked.connect(self.quitarListaEquipo)
        self.botonActualizarEqui.clicked.connect(self.actualizarEquiposClub)
        self.botonAceptar.clicked.connect(self.crearClub)
        #Llamar metodo para salir del sistema
        self.boton_salir.clicked.connect(self.salir)
        #Cargar los equipos al combobox y agentes libres en Modificar
        self.cargar_cbEquipos.clicked.connect(self.cargarComboModificar)
        #Cargar la plantilla del equipo seleccionado en el combo Modificar
        self.comboBox_7.currentIndexChanged.connect(self.cargarPlantillasModificar)
        #Agregar jugadores agentes libres a Equipo seleccionado
        self.pushButton_3.clicked.connect(self.agregarAgenteLibre)
        #Despedir jugador y volverlo agente libre
        self.pushButton_2.clicked.connect(self.despedirJugador)
        #Cargar equipos a la lista de crear temporada
        self.cargarEquiposTemp.clicked.connect(self.cargarEquiposTemporada)
        #Agregar equipos a la temporada nueva
        self.botonAgregarEquipo_2.clicked.connect(self.agregarEquiposTemporada)
        #Crear temporada
        self.botonCrearTemp.clicked.connect(self.crearTemporada)
        #Actualizar combobox temporadas
        self.botonTemporadas.clicked.connect(self.cargarComboTemporadas)
        

    #Metodo al accionar el boton de exit
    def salir(self):
        sys.exit()
        print ('Salir del sistema exitoso')
    
    def autenticar(self):
        input_username = str(self.username.text())
        input_password = str(self.password.text())
        if input_username == "admin":
            print ('Username encontrado')
            if  input_password == 'admin':
                print ('Password encontrado')
                self.Log_in_admin.setTabEnabled(1, True)
                self.Log_in_admin.setTabEnabled(2, True)
            else:
                print ('Password no encontrada')
        else:
            print ('Username no encontrado')

    def recuperarPersona(self):
        print ('Entro al metodo')
        fechaN = self.fecha_nacimiento.date()
        fechaN = fechaN.toPyDate()
        identidad = self.numero_dentidad.text()
        pNombre = self.primer_nombre.text()
        pApellido = self.primer_apellido.text()
        rol = str(self.combo_box_desempeno.currentText())
        peso = self.doubleSpinBox.value()
        print(fechaN)
        print(identidad)
        print(pNombre)
        print(pApellido)
        print(rol)
        print(peso)

        serverCDB = Server()
        db = serverCDB['quinelas']

        if identidad not in db:
            docPersona = {
                '_id': identidad,
                'content': {
                    'nombre': pNombre,
                    'apellido': pApellido,
                    'fechaN': fechaN.strftime('%m/%d/%Y'),
                    'rol': rol,
                    'peso': peso,
                    'equipo': "N/A"
                }
            }
            db.save(docPersona)
        else:
            print("Ya existe una persona con ese ID")
        #-----faltaria hacer el insert aqui-----

    def listarJugadores(self):
        serverCDB = Server()
        db = serverCDB['quinelas']

        lists = db.view('queries/getJugadoresSinEquipo')
        self.lista_jugadores_disp.clear()
        self.lista_jugadores_ag.clear()
        temporal = []
        for item in lists:
            docTemp = item.value
            print(docTemp['content']['nombre'])
            temporal.append(docTemp['_id'])
            jId = docTemp["_id"]
            jNombre = docTemp['content']['nombre']
            jApellido = docTemp['content']['apellido']
            #jFecha = docTemp['content']['fechaN']
            #jRol = docTemp['content']['rol']
            jPeso = docTemp['content']['peso']
            listRow = jId+"-"+jNombre+" "+jApellido+"-"+str(jPeso)
            self.lista_jugadores_disp.addItem(listRow)
        global listaJugadores
        listaJugadores = temporal
        global jugadoresAgregados
        jugadoresAgregados = []
            
    def insertarEquipo(self):
        print("INSERTAR EQUIPO")
        nEquipo = self.texto_nom_equipo.text()
        print(nEquipo)
        nClub = "N/A"
        global jugadoresAgregados
        nJugadores = jugadoresAgregados
        print("*******************")
        for i in range(0,len(nJugadores)):
            print(nJugadores[i])
        print("********************")
        
        serverCDB = Server()
        db = serverCDB['quinelas']
        
        if nEquipo not in db:
            print("entro aqui perro")
            docEquipo = {
                '_id': nEquipo,
                'content': {
                    'club': nClub,
                    'integrantes': nJugadores
                }
            }
            db.save(docEquipo)

            for id in nJugadores:
                jugador = db.get(id)
                jugador["content"]["equipo"] = nEquipo
                db.save(jugador)

            print("Agregado exitosamente!")
        else:
            print("Ya existe un equipo con ese ID")
        self.lista_jugadores_disp.clear()
        self.lista_jugadores_ag.clear()
        jugadoresAgregados = []

    def transferirJugadores(self):
        global jugadoresAgregados
        temporal = jugadoresAgregados
        for JugadorSelec in self.lista_jugadores_disp.selectedItems():
            #tempo = self.lista_jugadores_disp.currentItem()
            value = JugadorSelec.text()
            value = value.split("-")
            idSuazo = value[0]+"-"+value[1]+"-"+value[2]
            temporal.append(idSuazo)
            print(idSuazo)    
            self.lista_jugadores_disp.takeItem(self.lista_jugadores_disp.row(JugadorSelec))
            self.lista_jugadores_ag.addItem(JugadorSelec)
        #jugadoresAgregados.append(self.lista_jugadores_disp.currentRow())
        jugadoresAgregados = temporal
        #for i in range(0, len(temporal)):
        #    print(temporal[i])         
        #print(self.lista_jugadores_disp.currentRow())            
        
    def actualizarEquiposClub(self):
        self.listaEquiposSel.clear()
        self.listaEquiposDisp.clear()

        serverCDB = Server()
        db = serverCDB['quinelas']

        equiposSinClub = db.view('queries/getEquiposSinClub')

        for equipo in equiposSinClub:
            equipo = equipo.value
            row = equipo["_id"]
            print(row)
            self.listaEquiposDisp.addItem(row)
        """
        equiposSinClub = db.view('queries/getEquiposSinClub')

        for equipo in equiposSinClub:
            equipo = equipo.value
            row = equipo["_id"]
            if row.split("-")[0] == "2017"
                print(row)
                self.listaEquiposDisp.addItem(row)"""

    def agregarListaEquipo(self):
        for EquipoSelec in self.listaEquiposDisp.selectedItems():
            self.listaEquiposDisp.takeItem(self.listaEquiposDisp.row(EquipoSelec))
            self.listaEquiposSel.addItem(EquipoSelec)

    def quitarListaEquipo(self):
        for EquipoSelec in self.listaEquiposSel.selectedItems():
            self.listaEquiposSel.takeItem(self.listaEquiposSel.row(EquipoSelec))
            self.listaEquiposDisp.addItem(EquipoSelec)

    def crearClub(self):
        print("CREAR CLUB")

        serverCDB = Server()
        db = serverCDB['quinelas']

        idClub = "1" + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9))

        listaEquipos = []
        cont = 0

        items = [] 
        for index in range(self.listaEquiposSel.count()): 
            items.append(str(self.listaEquiposSel.item(index).text()))
        #Ejemplo de como modificar
        for EquipoSelec in items:
            #EquipoSelec = str(self.listaEquiposSel.item(cont))
            listaEquipos.append(EquipoSelec)
            docEquipo = db.get(EquipoSelec)
            docEquipo["content"]["club"] = idClub
            print(docEquipo)
            db.save(docEquipo)
            cont += 1

        docClub = {
            '_id': idClub,
            'content': {
                'equipos': listaEquipos
            }
        }
        db.save(docClub)

        self.listaEquiposSel.clear()
        self.listaEquiposDisp.clear()

    #Metodo para calcular el bioritmo promedio para un equipo
    def calcularBioritmos(self, equipoSelec):

        #Este metodo calcula el bioritmo para un EQUIPO
        #Calcula el bioritmo para cada jugador individual, los suma y saca la media ponderada
        #Luego, saca la media de los 3 bioritmos (fis, emo, int)

        """
        A partir de aqui, necesito saber los equipos y sus jugadores para calcular su bioritmo
        """
        print("CALCULAR BIORITMOS")

        serverCDB = Server()
        db = serverCDB['quinelas']
        acumPesos = 0
        acumFisico = 0
        acumEmo = 0
        acumIntel = 0
        if(equipoSelec in db):
            doc = db[equipoSelec]
            listaJ = []
            #listaJ = doc["content"]["integrantes"]
            for i in range(0,10):
                elementoI = listaJ[i]
                doc1 = db[elementoI]
                fechaNac = doc1["content"]["fechaN"]
                fechaNac = fechaNac.toPyDate()
                fechaAct = datetime.datetime.now().date()
                delta = fechaAct - fechaNac
                pesoAct = doc1["content"]["peso"]
                acumPesos += pesoAct
                #fisico = (100*math.sin((math.pi*2*delta.days)/23))*pesoAct
                acumFisico += (100*math.sin((math.pi*2*delta.days)/23))*pesoAct
                #emocional = (100*math.sin((math.pi*2*delta.days)/28))*pesoAct
                acumEmo += (100*math.sin((math.pi*2*delta.days)/28))*pesoAct
                #intelectual = (100*math.sin((math.pi*2*delta.days)/33))*pesoAct
                acumIntel += (100*math.sin((math.pi*2*delta.days)/33))*pesoAct
            mediaF = acumFisico/acumPesos
            mediaE = acumEmo/acumPesos
            mediaI = acumIntel/acumPesos
            mediaT = (mediaF+mediaE+mediaI)/3
            return mediaT                    
        else:
            print("Ese equipo no existe o no tiene jugadores")

    #Metodo que agrega los equipos al combobox en modificar
    def cargarComboModificar(self):
        #Limpiar las listas
        self.listWidget_2.clear()
        #Agregar los equipos al combobox
        self.comboBox_7.clear()
        serverCDB = Server()
        db = serverCDB['quinelas']
        equipos = db.view('queries/getEquipos')
        listaTemporal = []
        for equipo in equipos:
            equipo = equipo.value
            cbItem = equipo["_id"]
            listaTemporal.append(cbItem)
        self.comboBox_7.addItems(listaTemporal)
        self.cargarAgentesLibre()
        
    #Metodo que carga los jugadores Agentes Libre
    def cargarAgentesLibre(self):
        self.listWidget_2.clear()
        serverCDB = Server()
        db = serverCDB['quinelas']
        jugadores = db.view('queries/getJugadoresSinEquipo')
        for jugador in jugadores:
            docTemp = jugador.value
            listRow = docTemp["_id"]+"-"+docTemp["content"]["nombre"]+"-"+docTemp["content"]["apellido"]+"-"+str(docTemp["content"]["peso"])
            self.listWidget_2.addItem(listRow)  
    
    #Metodo que carga los jugadores del equipo seleccionado del cb en Modificar
    def cargarPlantillasModificar(self):
        self.listWidget.clear()
        print("PLANTILLAS EQUIPOS")
        serverCDB = Server()
        db = serverCDB['quinelas']
        #Agregar los jugadores del equipo seleccionado cb
        equipoKey = str(self.comboBox_7.currentText())
        equipo = db[equipoKey]
        jugadores = equipo["content"]["integrantes"]
        for jugador in jugadores:
            actual = db[jugador]
            listRow = actual["_id"]+"-"+actual["content"]["nombre"]+"-"+actual["content"]["apellido"]+"-"+str(actual["content"]["peso"])
            self.listWidget.addItem(listRow)

    #Metodo que agrega al equipo un jugador agente libre
    def agregarAgenteLibre(self):
        if(len(self.listWidget_2.selectedItems())>0):
            listaNuevos = []
            serverCDB = Server()
            db = serverCDB['quinelas']
            for jugador in self.listWidget_2.selectedItems():
                value = jugador.text()
                value = value.split("-")
                idJ = value[0]+"-"+value[1]+"-"+value[2]
                listaNuevos.append(idJ)
                docJugador = db[idJ]
                docJugador["content"]["equipo"] = str(self.comboBox_7.currentText())
                db.save(docJugador)       
                self.listWidget_2.takeItem(self.listWidget_2.row(jugador))
            equipoKey = str(self.comboBox_7.currentText())
            equipo = db[equipoKey]
            plantillaAct = equipo["content"]["integrantes"]
            plantillaAct = plantillaAct + listaNuevos
            equipo["content"]["integrantes"] = plantillaAct
            db.save(equipo)
            self.cargarPlantillasModificar()
        else:
            print("ERROR! Debe elegir un elemento de la lista Agente Libre")

    #Metodo que despide a un jugador del equipo en Modificar
    def despedirJugador(self):
        if(len(self.listWidget.selectedItems()) > 0):
            serverCDB = Server()
            db = serverCDB['quinelas']
            equipo = db[str(self.comboBox_7.currentText())]
            plantillaAct = equipo["content"]["integrantes"]
            for jugador in self.listWidget.selectedItems():
                value = jugador.text()
                value = value.split("-")
                idJ = value[0]+"-"+value[1]+"-"+value[2]
                plantillaAct.remove(idJ)
                docJ = db[idJ]
                docJ["content"]["equipo"]="N/A"
                db.save(docJ)
                self.listWidget.takeItem(self.listWidget.row(jugador))
            equipo["content"]["integrantes"] = plantillaAct
            db.save(equipo)
            self.cargarAgentesLibre()
        else:
            print("ERROR! Debe elegir un elemento de la lista Plantilla")
        
    def cargarEquiposTemporada(self):
        self.equiposDisp.clear()
        self.equiposPart.clear()
        serverCDB = Server()
        db = serverCDB['quinelas']
        equipos = db.view('queries/getEquipos')
        listaTemporal = []
        for equipo in equipos:
            equipo = equipo.value
            IDEquipo = equipo["_id"]
            listaTemporal.append(IDEquipo)
            self.equiposDisp.addItem(IDEquipo)

    def agregarEquiposTemporada(self):
        for EquipoSelec in self.equiposDisp.selectedItems():
            self.equiposDisp.takeItem(self.equiposDisp.row(EquipoSelec))
            self.equiposPart.addItem(EquipoSelec)

    def crearTemporada(self):
        serverCDB = Server()
        db = serverCDB['quinelas']

        if len(self.texIntTemporada.text()) > 0:
            anoTemp = self.texIntTemporada.text()
            equipos = [] 
            for index in range(self.equiposPart.count()): 
                equipos.append(str(self.equiposPart.item(index).text()))

            for id_equipo in equipos:
                equipo = db.get(id_equipo)
                #saca el club del equipo
                club = db.get(equipo["content"]["club"])
                if club == "N/A":
                    print("ERROR! Equipo sin Club")
                    return

            docTemp = {
                "_id": anoTemp,
                "content":{
                    "equipos": equipos
                }
            }

            db.save(docTemp)
            
            contador_jornada =1

            #existe una lista de los enfrentamientos ya disputados donde no pueden disputarse mas de 1 vez por temporada
            #def enfrentamientos(self):  
            lista_partidos_totales =[]
            #cada jornada tiene 14 partidos (n-1)
            jornada =contador_jornada
            #existen equipos locales y visitantes 
            for i in range(len(equipos)):
                lista_partidos = []
                while len(lista_partidos) <14:
                    ran1=randint(0,len(equipos)-1)
                    ran2=randint(0,len(equipos)-1)
                    partido = equipos[ran1]+"-"+equipos[ran2]
                    if partido not in lista_partidos_totales:
                        print ("No se ha jugado en otra fecha")
                        lista_partidos_totales.append(partido)
                        if partido not in lista_partidos:
                            print ("No se ha jugado esta jornada")
                            lista_partidos.append(partido)
                        else:
                            print ("El partido ya se jugo en esta jornada ")
                    else:
                        print ('El partido ya se jugo en otra fecha aparentemente')
                
                print ("Jornada-> " + str(contador_jornada))
                print ("Lista partidos:")
                #for j in len(lista_partidos):
                #    print 'Juego:'+j+" "+lista_partidos[j]
                print (lista_partidos)

                #Escoger Jugadores
                for encuentro in lista_partidos:
                    #Validacion por si dos equipos del mismo club se enfrentan
                    listaJugadoresUsados = []

                    #----------Local-------------

                    id_equipo = encuentro.split("-")[0]
                    print(id_equipo)
                    equipo = db.get(id_equipo)
                    #saca el club del equipo
                    club = db.get(equipo["content"]["club"])
                    print(equipo["content"]["club"])

                    jugadores_temp = []

                    #saca los equipos del club
                    for equipoClub in club["content"]["equipos"]:
                        equipoClub = db.get(equipoClub)
                        #saca los integrantes de los equipos
                        for jugadorClub in equipoClub["content"]["integrantes"]:
                            #y lo agrega
                            jugadores_temp.append(jugadorClub)

                    #agrega los tutulares random
                    jugadores_Titulares = []
                    for i in range(11):
                        jugRan = randint(0, len(jugadores_temp)-1)
                        jugadores_Titulares.append(jugadores_temp[jugRan])
                        listaJugadoresUsados.append(jugadores_temp[jugRan])
                        jugadores_temp.pop(jugRan)

                    #agrega los suplentes random
                    jugadores_Suplentes = []
                    for i in range(5):
                        jugRan = randint(0, len(jugadores_temp)-1)
                        jugadores_Suplentes.append(jugadores_temp[jugRan])
                        listaJugadoresUsados.append(jugadores_temp[jugRan])
                        jugadores_temp.pop(jugRan)

                    tecnicoE = db.view("queries/getEntrenador")
                    #tecnicoE = tecnicoE[randint(0,len(tecnicoE))]
                    tecnicoEs = []
                    for tec in tecnicoE:
                        tec = tec.key
                        tecnicoEs.append(tec)

                    foo = randint(0, len(tecnicoEs) - 1)
                    print(tecnicoEs[foo])
                    vari = tecnicoEs[foo]

                    #Crea el doc con toda la info necesaria
                    docLocal = {
                        "nombre": equipo["_id"],
                        "jugadores_titulares": jugadores_Titulares,
                        "jugadores_suplentes": jugadores_Suplentes,
                        "entrenador": vari
                    }

                    #----------Visita---------

                    id_equipo = encuentro.split("-")[1]
                    equipo = db.get(id_equipo)
                    #saca el club del equipo
                    club = db.get(equipo["content"]["club"])

                    jugadores_temp = []

                    #saca los equipos del club
                    for equipoClub in club["content"]["equipos"]:
                        equipoClub = db.get(equipoClub)
                        #saca los integrantes de los equipos
                        for jugadorClub in equipoClub["content"]["integrantes"]:
                            #y lo agrega

                            #con la condicion extra
                            if jugadorClub not in listaJugadoresUsados:
                                jugadores_temp.append(jugadorClub)

                    #agrega los tutulares random
                    jugadores_Titulares = []
                    for i in range(11):
                        jugRan = randint(0, len(jugadores_temp)-1)
                        jugadores_Titulares.append(jugadores_temp[jugRan])
                        listaJugadoresUsados.append(jugadores_temp[jugRan])
                        jugadores_temp.pop(jugRan)

                    #agrega los suplentes random
                    jugadores_Suplentes = []
                    for i in range(5):
                        jugRan = randint(0, len(jugadores_temp)-1)
                        jugadores_Suplentes.append(jugadores_temp[jugRan])
                        listaJugadoresUsados.append(jugadores_temp[jugRan])
                        jugadores_temp.pop(jugRan)

                    tecnicoE = db.view("queries/getEntrenador")
                    #tecnicoE = tecnicoE[randint(0,len(tecnicoE))]
                    tecnicoEs = []
                    for tec in tecnicoE:
                        tec = tec.key
                        tecnicoEs.append(tec)

                    foo = randint(0, len(tecnicoEs) - 1)
                    print(tecnicoEs[foo])
                    vari = tecnicoEs[foo]

                    #Crea el doc con toda la info necesaria
                    docVisita = {
                        "nombre": equipo["_id"],
                        "jugadores_titulares": jugadores_Titulares,
                        "jugadores_suplentes": jugadores_Suplentes,
                        "entrenador": vari
                    }

                    arbitros = []
                    listaArbitrosV = db.view("queries/getArbitros")
                    listaArbitros = []
                    for arb in listaArbitrosV:
                        listaArbitros.append(arb.key)

                    for i in range(4):
                        posArbitro = randint(0, len(listaArbitros) - 1)
                        arbitros.append(listaArbitros[posArbitro])
                        listaArbitros.pop(posArbitro)

                    #FINALMENTE EL DOC DE PARTIDO

                    docPartido = {
                        "_id": str(anoTemp) + "-" + str(contador_jornada) + "-" + encuentro.split("-")[0] + "-" + encuentro.split("-")[1],
                        "content":{
                            "jornada": contador_jornada,
                            "local": docLocal,
                            "visita": docVisita,
                            "arbitros": arbitros,
                            "score_local": "N/A",
                            "score_visita": "N/A"

                        }
                    }
                    db.save(docPartido)

                contador_jornada+=1

    #Metodo para cargar los años de las temporadas en el combo en Jugar
    def cargarComboTemporadas(self):
        serverCDB = Server()
        db = serverCDB['quinelas']
        #NO SE COMO SE LLAMA ESTA VIEW, NO TENGO COUCH!
        temporadas = db.view('queries/getPartidas')
        #FIN DEL COMUNICADO
        listaYrs = []
        for temporada in temporadas:
            docTemp = temporada.value
            idT = docTemp["_id"]
            listaTempo = idT.split("-")
            idT = listaTempo[0]
            if idT not in listaYrs:
                listaYrs.append(idT)
        self.comboBox.addItems(listaYrs)



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())