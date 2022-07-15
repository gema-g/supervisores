#renderisar el template y configurar el uso de Flask
from flask import Flask, Response
from flask import render_template, request, redirect, url_for, flash #diseño
#importar la base de datos
from flaskext.mysql import MySQL 
from datetime import datetime #nombre de la foto de acuerdo al tiempo
import os #importar modulo para entrar directamente a la carpeta de uploads y actualizarlo
import sys  #sistema
from flask import send_from_directory
import pymysql
from fpdf import FPDF #generar pdf

date=datetime.now()

app= Flask(__name__)
app.secret_key="Develoteca" 

#proceso para la conexion con la base de datos
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='bdb1'
mysql.init_app(app)

#Referencia a la carpeta uploads con la configuracion de Phyton para guardar la ruta como un valor de la carpeta
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

#la aplicación recibira solicitudes mediante la URL (host)
#Mostrar datos de la base de datos 
@app.route('/')
def index():

    sql="SELECT * FROM `info_tecnicos`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    
    infot=cursor.fetchall()
    print(infot)
    
    conn.commit()
    #accedera directamente a index.html | Enviar la información a la ventana de index 
    return render_template('tecnicos/index.html',info_tecnicos=infot)

#imprimir PDF por registro
@app.route('/downloadd/reportt/pdff/<int:id>')
def downloadd_reportt(id):
          now=date.today()
          conn= mysql.connect()
          cursor= conn.cursor(pymysql.cursors.DictCursor)

          #cursor.execute("SELECT fotografia,nombre,num_empleado,unidad,num_dimme,nom_emergencia,num_emergencia,vigencia FROM info_tecnicos")
          cursor.execute("SELECT * FROM info_tecnicos WHERE id=%s", id)
          result= cursor.fetchall()

          pdf = FPDF()
          pdf = FPDF('P', 'mm', (300, 400))
          pdf.add_page()

          page_width =pdf.w - 2 * pdf.l_margin
          
          pdf.ln(7)
          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'MEGACABLE COMUNICACIONES S.A. DE C.V.', align='C')
          pdf.ln(8)

          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'---Atención Domiciliaria---', align='C')
          pdf.ln(4)

          absolutepath = os.path.abspath(__file__)
          fileDirectory = os.path.dirname(absolutepath)
          newPath2 = os.path.join(fileDirectory,'logo.jpg')   
          pdf.image(newPath2,x=12,y=8,w=45,h=35)
          pdf.ln(5)

          pdf.set_font('Times','B',12.0)
          pdf.cell(page_width,0.0,'Reporte: ', align='C')
          pdf.ln(6)

          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'"INFORMACIÓN DE TÉCNICOS"', align='C')
          pdf.ln(13)

          pdf.set_font('Times','B',12.0)
          pdf.cell(page_width,0.0,'Fecha: '+str(date.strftime("%d / %m / %y")), align='L')
          pdf.ln(5)
          
          pdf.set_font('Courier','B',12)

          col_width=page_width/10

          pdf.ln(1)

          th =pdf.font_size*5
          i=1
          s=th
          for row in result:
              pdf.cell(col_width * 3,40,"N°:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['id']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"CUADRILLA:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['cuadrilla']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"FOTOGRAFIA:", border=0, align= 'L')
              absolutepath = os.path.abspath(__file__)
              fileDirectory = os.path.dirname(absolutepath)
              newPath = os.path.join(fileDirectory, 'uploads',row['fotografia'])   
              pdf.cell(col_width * 4, 40,"",border=0, align= 'L')
              pdf.image(newPath,x=col_width * 4, y=80+s,w=30,h=28)
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"NOMBRE:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['nombre']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"N° EMPLEADO:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['num_empleado']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"N° CELULAR:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['num_celular']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"UNIDAD:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['unidad']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"SUPERVISOR:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['supervisor']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"N° DIMME:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['num_dimme']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"CURP:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['curp']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"RFC:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['rfc']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"SUCURSAL:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['sucursal']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"DIRECCIÓN:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['direccion']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"CORREO ELECT.:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['correo_elect']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"ESTADO CIVIL:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['estado_civil']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"NOMBRE DE EMERGENCIA:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['nom_emergencia']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"N° EMERG.:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['num_emergencia']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"N° DE LICENCIA:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['num_licencia']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"VIGENCIA:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['vigencia']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','',12)
              #pdf.cell(col_width-25, th, str(i), border=0, align= 'L')
              i=i+1
              s=s+25
              pdf.ln(th)

          pdf.ln(10)

          pdf.set_font('Times','',10.0)
          pdf.cell(page_width, 0.0, '- end of report -', align='C')

          return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=tecnicos_reportes_personal.pdf'}) #reporte_tecnico
          cursor.close()
          conn.commit()

#imprimir PDF
@app.route('/download/report/pdf')
def download_report():
          now=date.today()
          conn= mysql.connect()
          cursor= conn.cursor(pymysql.cursors.DictCursor)

          #cursor.execute("SELECT fotografia,nombre,num_empleado,unidad,num_dimme,nom_emergencia,num_emergencia,vigencia FROM info_tecnicos")
          cursor.execute("SELECT * FROM info_tecnicos")
          result= cursor.fetchall()

          pdf = FPDF()
          pdf = FPDF('P', 'mm', (400, 300))
          pdf.add_page()
          
          page_width =pdf.w - 2 * pdf.l_margin

          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'MEGACABLE COMUNICACIONES S.A. DE C.V.', align='C')
          pdf.ln(8)

          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'---Atención Domiciliaria---', align='C')
          pdf.ln(4)

          absolutepath = os.path.abspath(__file__)
          fileDirectory = os.path.dirname(absolutepath)
          newPath2 = os.path.join(fileDirectory,'logo.jpg')   
          pdf.image(newPath2,x=12,y=8,w=45,h=35)
          pdf.ln(5)

          pdf.set_font('Times','B',12.0)
          pdf.cell(page_width,0.0,'Reporte: ', align='C')
          pdf.ln(6)

          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'"INFORMACIÓN DE TÉCNICOS"', align='C')
          pdf.ln(13)

          pdf.set_font('Times','B',12.0)
          pdf.cell(page_width,0.0,'Fecha: '+str(date.strftime("%d / %m / %y")), align='L')
          pdf.ln(5)
          
          pdf.set_font('Courier','B',12)

          col_width=page_width/9

          pdf.ln(1)

          th =pdf.font_size*6
          t=1
          pdf.cell(col_width-25,th,"N°", border=1, ln=0, align= 'C')
          pdf.cell(col_width,th,"FOTOGRAFIA", border=1, ln=0, align= 'C')
          pdf.cell(col_width+45,th,"NOMBRE", border=1, ln=0, align= 'C')
          pdf.cell(col_width-10,th,"N° EMPLEADO", border=1, ln=0, align= 'C')
          pdf.cell(col_width-10,th,"UNIDAD", border=1, ln=0, align= 'C')
          pdf.cell(col_width-10,th,"N° DIMME", border=1, ln=0, align= 'C')
          pdf.cell(col_width+30,th,"NOMBRE DE EMERGENCIA", border=1, ln=0, align= 'C')
          pdf.cell(col_width-10,th,"N° EMERG.", border=1, ln=0, align= 'C')
          pdf.cell(col_width-10,th,"VIGENCIA", border=1, ln=0, align= 'C')
          pdf.ln(th)
          i=th
          y=0
          #s=th
          for row in result:
              pdf.set_font('Courier','',12)
              pdf.cell(col_width-25, th, str(t), border=1, align= 'L')
              #pdf.cell(col_width-25,th,str(row['id']),border=1, ln=0, align='L')
              absolutepath = os.path.abspath(__file__)
              fileDirectory = os.path.dirname(absolutepath)
              newPath = os.path.join(fileDirectory, 'uploads',row['fotografia'])   
              pdf.cell(col_width, th, "",border=1, ln=0, align= 'L')
              pdf.image(newPath,x=col_width-10,y=48+i,w=30,h=32)
              pdf.cell(col_width+45, th, str(row['nombre']), border=1, ln=0, align= 'L')
              pdf.cell(col_width-10, th, str(row['num_empleado']), border=1, ln=0, align= 'L')
              pdf.cell(col_width-10, th, str(row['unidad']), border=1, ln=0, align= 'L')
              pdf.cell(col_width-10, th, str(row['num_dimme']), border=1, ln=0, align= 'L')
              pdf.cell(col_width+30, th, str(row['nom_emergencia']), border=1, ln=0, align= 'L')
              pdf.cell(col_width-10, th, str(row['num_emergencia']), border=1, ln=0, align= 'L')
              pdf.cell(col_width-10, th, str(row['vigencia']), border=1, ln=1, align= 'L')
              
              textid = str(row['id'])
              textfoto = '                  '
              textnombre=str(row['nombre'])
              textnempleado=str(row['num_empleado'])
              textunidad=str(row['unidad'])
              textndimme=str(row['num_dimme'])
              textnomeme=str(row['nom_emergencia'])
              textnumeme=str(row['num_emergencia'])
              textvigencia=str(row['vigencia'])
              i=i+26
              if(i >= 190):
                  i=th-68
                  pdf.add_page()
              t=t+1
              #s=s+25
              #pdf.ln(th)

          pdf.ln(10)

          pdf.set_font('Times','',10.0)
          pdf.cell(page_width, 0.0, '- end of report -', align='C')
          
          return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=tecnicos_reportes.pdf'}) #reporte_tecnicos

          cursor.close()
          conn.commit()

    
@app.route('/destroy/<int:id>')
def destroy(id):
    conn= mysql.connect()
    cursor= conn.cursor()

    #cursor.execute("SELECT fotografia FROM info_tecnicos WHERE id=%s", id)
    #fila=cursor.fetchall()
    #os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))

    cursor.execute("DELETE FROM info_tecnicos WHERE id=%s", (id))
    conn.commit()
    return redirect('http://20.114.233.203/')

@app.route('/edit/<int:id>')
def edit(id):
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM info_tecnicos WHERE id=%s", (id))
    infot=cursor.fetchall()   
    conn.commit()
    print(infot)
    
    return render_template('tecnicos/edit.html',info_tecnicos=infot)
#-------------
@app.route('/datos/<int:id>')
def datos(id):
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM info_tecnicos WHERE id=%s", (id))
    infot=cursor.fetchall()   
    conn.commit()
    print(infot)
    
    return render_template('tecnicos/datos.html',info_tecnicos=infot)
#-------------
@app.route('/update',  methods=['POST'])
def update():
    _cuadrilla=request.form['txtCuadrilla']
    _nombre=request.form['txtNombre']
    _numeroe=request.form['txtNumeroE']
    _numeroc=request.form['txtNumeroC']
    _unidad=request.form['txtUnidad']
    _supervisor=request.form['txtSupervisor']
    _numerod=request.form['txtNumeroD']
    _curp=request.form['txtCurp']
    _rfc=request.form['txtRfc']
    _sucursal=request.form['txtSucursal']
    _direccion=request.form['txtDireccion']
    _correoe=request.form['txtCorreoE']
    _estadoc=request.form['txtEstadoC']
    _nombree=request.form['txtNombreE']
    _numeroem=request.form['txtNumeroEm']
    _numerol=request.form['txtNumeroL']
    _vigencia=request.form['txtVigencia']
    _foto=request.files['txtFoto']
    id=request.form['txtID']

    sql="UPDATE info_tecnicos SET cuadrilla=%s, nombre=%s, num_empleado=%s, num_celular=%s, unidad=%s, supervisor=%s, num_dimme=%s, curp=%s, rfc=%s, sucursal=%s, direccion=%s, correo_elect=%s, estado_civil=%s, nom_emergencia=%s, num_emergencia=%s, num_licencia=%s, vigencia=%s WHERE id=%s ;"
    
    datos=(_cuadrilla, _nombre, _numeroe, _numeroc, _unidad, _supervisor, _numerod, _curp, _rfc, _sucursal, _direccion, _correoe, _estadoc, _nombree, _numeroem,_numerol, _vigencia, id)
    
    conn= mysql.connect()
    cursor=conn.cursor()
    
    #nombre que recibe la imagen 
    now= datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    #subir la imagen a la base de datos 
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+ nuevoNombreFoto) 

        cursor.execute("SELECT fotografia FROM info_tecnicos WHERE id=%s", id)
        fila=cursor.fetchall()
        
        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute("UPDATE info_tecnicos SET fotografia=%s WHERE id=%s",(nuevoNombreFoto,id))
        conn.commit()

    cursor.execute(sql,datos)
    conn.commit()

    return redirect('http://20.114.233.203/')
    #return render_template('tecnicos/index.html',info_tecnicos=infot)
    
@app.route('/create')
def create():
    return render_template('tecnicos/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _cuadrilla=request.form['txtCuadrilla']
    _nombre=request.form['txtNombre']
    _numeroe=request.form['txtNumeroE']
    _numeroc=request.form['txtNumeroC']
    _unidad=request.form['txtUnidad']
    _supervisor=request.form['txtSupervisor']
    _numerod=request.form['txtNumeroD']
    _curp=request.form['txtCurp']
    _rfc=request.form['txtRfc']
    _sucursal=request.form['txtSucursal']
    _direccion=request.form['txtDireccion']
    _correoe=request.form['txtCorreoE']
    _estadoc=request.form['txtEstadoC']
    _nombree=request.form['txtNombreE']
    _numeroem=request.form['txtNumeroEm']
    _numerol=request.form['txtNumeroL']
    _vigencia=request.form['txtVigencia']
    _foto=request.files['txtFoto']

    if _cuadrilla=='' or _foto=='' or _nombre=='' or _numeroe=='' or _numeroc=='' or _unidad=='' or _supervisor=='' or _numerod=='' or _curp=='' or _rfc=='' or _sucursal=='' or _direccion=='' or _correoe=='' or _estadoc=='' or _nombree=='' or _numeroem=='' or _numerol=='' or _vigencia=='': 
        flash('Recuerda llenar todos los datos de los campos') 
        return redirect(url_for('create'))   

    now= datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+ nuevoNombreFoto) 

    sql="INSERT INTO `info_tecnicos` (`id`, `cuadrilla`, `fotografia`, `nombre`, `num_empleado`, `num_celular`, `unidad`, `supervisor`, `num_dimme`, `curp`, `rfc`, `sucursal`, `direccion`, `correo_elect`, `estado_civil`, `nom_emergencia`, `num_emergencia`, `num_licencia`, `vigencia`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    
    datos=(_cuadrilla,nuevoNombreFoto, _nombre, _numeroe, _numeroc, _unidad, _supervisor, _numerod, _curp, _rfc, _sucursal, _direccion, _correoe, _estadoc, _nombree, _numeroem,_numerol, _vigencia)
    
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    #accedera directamente a index.html
    return redirect('http://20.114.233.203/')

#--------------------------- INFO_VEHICULOS ----------------------
#la aplicación recibira solicitudes mediante la URL (host)
@app.route('/ivehiculos')
def indexit():

    sql="SELECT * FROM `info_vehiculos`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    
    infov=cursor.fetchall()
    print(infov)
    
    conn.commit()
    #accedera directamente a index.html | Enviar la información a la ventana de index 
    return render_template('vehiculos/indexit.html',info_vehiculos=infov)

@app.route('/createiv')
def createiv():
    return render_template('vehiculos/createiv.html')
    
@app.route('/storeiv', methods=['POST'])
def storageiv():
    _unidadv=request.form['txtUnidadV']
    _año=request.form['txtAño']
    _cuadrillav=request.form['txtCuadrillaV']
    _numeroec=request.form['txtNumeroEc']
    _numeros=request.form['txtNumeroS']
    _tarjeta=request.form['txtTarjeta']
    _nip=request.form['txtNip']
    _tipo=request.form['txtTipo']

    if _unidadv=='' or _año=='' or _cuadrillav=='' or _numeroec=='' or _numeros=='' or _tarjeta=='' or _nip=='' or _tipo=='':
        flash('Recuerda llenar todos los datos de los campos') 
        return redirect(url_for('createiv'))   
    

    sql="INSERT INTO `info_vehiculos` (`id`, `unidad`, `año`, `cuadrilla`, `num_econ`, `num_serie`, `tarjeta`, `nip`, `tipo`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s);"
    
    datosiv=(_unidadv, _año, _cuadrillav, _numeroec, _numeros, _tarjeta, _nip, _tipo)
    
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datosiv)
    conn.commit()
    
    #return render_template('vehiculos/indexit.html')
    return redirect('http://20.114.233.203/ivehiculos')

#imprimir PDF por registro

#imprimir PDF
@app.route('/downloadv/reportv/pdfv')
def download_reportv():
          now=date.today()
          conn= mysql.connect()
          cursor= conn.cursor(pymysql.cursors.DictCursor)

          #cursor.execute("SELECT unidad,año,cuadrilla,num_serie,num_econ,tarjeta,nip,tipo FROM info_vehiculos")
          cursor.execute("SELECT * FROM info_vehiculos")
          result= cursor.fetchall()
          
          pdf = FPDF()
          pdf = FPDF('P', 'mm', (300, 200))
          pdf.add_page()
          
          page_width =pdf.w - 2 * pdf.l_margin

          pdf.ln(7)
          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'MEGACABLE COMUNICACIONES S.A. DE C.V.', align='C')
          pdf.ln(8)

          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'---Atención Domiciliaria---', align='C')
          pdf.ln(4)

          absolutepath = os.path.abspath(__file__)
          fileDirectory = os.path.dirname(absolutepath)
          newPath2 = os.path.join(fileDirectory,'logo.jpg')   
          pdf.image(newPath2,x=12,y=8,w=45,h=35)
          pdf.ln(5)


          pdf.set_font('Times','B',12.0)
          pdf.cell(page_width,0.0,'Reporte: ', align='C')
          pdf.ln(6)

          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'"INFORMACIÓN DE VEHICULOS"', align='C')
          pdf.ln(13)

          pdf.set_font('Times','B',12.0)
          pdf.cell(page_width,0.0,'Fecha: '+str(date.strftime("%d / %m / %y")), align='L')
          pdf.ln(5)
          
          pdf.set_font('Courier','B',12)
          #pdf.set_font('Courier','',12)

          col_width=page_width/9

          pdf.ln(1)

          th = pdf.font_size*2
          i=1
          pdf.cell(col_width-10,th,"N°", border=1)
          pdf.cell(col_width,th,"UNIDAD", border=1)
          pdf.cell(col_width-10,th,"AÑO", border=1)
          pdf.cell(col_width+5,th,"CUADRILLA", border=1)
          pdf.cell(col_width,th,"N° ECONOM.", border=1)
          pdf.cell(col_width+10,th,"N° DE SERIE", border=1)
          pdf.cell(col_width+10,th,"TARJETA", border=1)
          pdf.cell(col_width-10,th,"NIP", border=1)
          pdf.cell(col_width-10,th,"TIPO", border=1)
          pdf.ln(th)
          for row in result:
              pdf.set_font('Courier','',12)
              pdf.cell(col_width-10, th, str(i), border=1)
              pdf.cell(col_width,th, str(row['unidad']), border=1)
              pdf.cell(col_width-10,th, row['año'], border=1)
              pdf.cell(col_width+5,th, row['cuadrilla'], border=1)
              pdf.cell(col_width,th, row['num_econ'], border=1)
              pdf.cell(col_width+10, th, row['num_serie'], border=1)
              pdf.cell(col_width+10, th, row['tarjeta'], border=1)
              pdf.cell(col_width-10, th, row['nip'], border=1)
              pdf.cell(col_width-10, th, row['tipo'], border=1)
              i=i+1
              pdf.ln(th)

          pdf.ln(10)

          pdf.set_font('Times','',10.0)
          pdf.cell(page_width, 0.0, '- end of report -', align='C')
          
          return Response(pdf.output(dest='S').encode('latin-1'), mimetype='applicationv/pdfv', headers={'Content-Disposition':'attachment;filename=vehiculos.pdf'})#reporte_vehiculos.pdf

          cursor.close()
          conn.commit()

@app.route('/destroyiv/<int:id>')
def destroyiv(id):
    conn= mysql.connect()
    cursor= conn.cursor()

    cursor.execute("DELETE FROM info_vehiculos WHERE id=%s", (id))
    conn.commit()
    return redirect('http://20.114.233.203/ivehiculos')

@app.route('/editiv/<int:id>')
def editiv(id):
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM info_vehiculos WHERE id=%s", (id))
    infov=cursor.fetchall()   
    conn.commit()
    print(infov)
    
    return render_template('vehiculos/editiv.html',info_vehiculos=infov)

@app.route('/datosv/<int:id>')
def datosv(id):
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM info_vehiculos WHERE id=%s", (id))
    infov=cursor.fetchall()   
    conn.commit()
    print(infov)
    
    return render_template('vehiculos/datosv.html',info_vehiculos=infov)

@app.route('/updateiv', methods=['POST'])
def updateiv():
    _unidadv=request.form['txtUnidadV']
    _año=request.form['txtAño']
    _cuadrillav=request.form['txtCuadrillaV']
    _numeroec=request.form['txtNumeroEc']
    _numeros=request.form['txtNumeroS']
    _tarjeta=request.form['txtTarjeta']
    _nip=request.form['txtNip']
    _tipo=request.form['txtTipo']
    idv=request.form['txtIDv']

    sql="UPDATE info_vehiculos SET unidad=%s, año=%s, cuadrilla=%s, num_econ=%s, num_serie=%s, tarjeta=%s, nip=%s, tipo=%s WHERE id=%s;"
    
    datosiv=(_unidadv, _año, _cuadrillav, _numeroec, _numeros, _tarjeta, _nip, _tipo, idv)
    
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datosiv)
    conn.commit()
    
    return redirect('http://20.114.233.203/ivehiculos')


#-----------------------INFO_DIMMES--------------------
#la aplicación recibira solicitudes mediante la URL (host)
@app.route('/idimmes')
def indexid():

    sql="SELECT * FROM `info_dimmes`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    
    infod=cursor.fetchall()
    print(infod)
    
    conn.commit()
    #accedera directamente a index.html | Enviar la información a la ventana de index 
    return render_template('dimmes/indexid.html',info_dimmes=infod)

@app.route('/createid')
def createid():
    
    return render_template('dimmes/createid.html')

@app.route('/storeid', methods=['POST'])
def storageid():
    _cuadrillad=request.form['txtCuadrillaD']
    _etiqueta=request.form['txtEtiqueta']
    _numerodi=request.form['txtNumeroDi']
    _imei1=request.form['txtImei1']
    _imei2=request.form['txtImei2']
    _modelo=request.form['txtModelo']
    _serie=request.form['txtSerie']
    _nombred=request.form['txtNombreD']
    _imeis=request.form['txtImeiS']
    _observaciones=request.form['txtObservaciones']
    _pantalla=request.form['txtPantalla']
    _fallas=request.form['txtFallas']
    _completas=request.form['txtCompletas']

    if _cuadrillad=='' or _etiqueta=='' or _numerodi=='' or _imei1=='' or _imei2=='' or _modelo=='' or _serie=='' or _nombred=='' or _imeis=='' or _observaciones=='' or _pantalla=='' or _fallas=='' or _completas=='':
        flash('Recuerda llenar todos los datos de los campos') 
        return redirect(url_for('createid'))   
    

    sql="INSERT INTO `info_dimmes` (`id`, `cuadrilla`, `etiqueta`, `numero`, `imei_1`, `imei_2`, `modelo`, `serie`, `nombre`, `imei_sim`, `observaciones`, `pantalla`, `fallas_atender`, `completas`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    
    datosid=(_cuadrillad, _etiqueta, _numerodi, _imei1, _imei2, _modelo, _serie, _nombred, _imeis, _observaciones, _pantalla, _fallas, _completas)
    
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datosid)
    conn.commit()
    
    #return render_template('vehiculos/indexit.html')
    return redirect('http://20.114.233.203/idimmes')

#imprimir PDF por registro
@app.route('/downloaddi/reportdi/pdfdi/<int:id>')
def download_reportddi(id):
          now=date.today()
          conn= mysql.connect()
          cursor= conn.cursor(pymysql.cursors.DictCursor)

          #cursor.execute("SELECT fotografia,nombre,num_empleado,unidad,num_dimme,nom_emergencia,num_emergencia,vigencia FROM info_tecnicos")
          cursor.execute("SELECT * FROM info_dimmes WHERE id=%s", id)
          result= cursor.fetchall()
          
          pdf = FPDF()
          pdf = FPDF('P', 'mm', (300, 400))
          pdf.add_page()

          page_width =pdf.w - 2 * pdf.l_margin
          
          pdf.ln(8)
          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'MEGACABLE COMUNICACIONES S.A. DE C.V.', align='C')
          pdf.ln(8)

          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'---Atención Domiciliaria---', align='C')
          pdf.ln(4)

          absolutepath = os.path.abspath(__file__)
          fileDirectory = os.path.dirname(absolutepath)
          newPath2 = os.path.join(fileDirectory,'logo.jpg')   
          pdf.image(newPath2,x=12,y=8,w=45,h=35)
          pdf.ln(5)

          pdf.set_font('Times','B',12.0)
          pdf.cell(page_width,0.0,'Reporte: ', align='C')
          pdf.ln(6)

          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'"INFORMACIÓN DE DIMME"', align='C')
          pdf.ln(13)

          pdf.set_font('Times','B',12.0)
          pdf.cell(page_width,0.0,'Fecha: '+str(date.strftime("%d / %m / %y")), align='L')
          pdf.ln(5)
          
          pdf.set_font('Courier','B',12)
          #pdf.set_font('Courier','',12)

          col_width=page_width/9

          pdf.ln(1)
          th = pdf.font_size*2.4
          i=1
          for row in result:
              pdf.cell(col_width * 3,40,"N°:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['id']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"CUADRILLA:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['cuadrilla']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"ETIQUETA:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['etiqueta']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"NUMERO:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['numero']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"IMEI 1:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['imei_1']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"IMEI_2:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['imei_2']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"MODELO:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['modelo']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"SERIE:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['serie']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"NOMBRE:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['nombre']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"IMEI SIM:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['imei_sim']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"OBSERVACIONES:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['observaciones']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"PANTALLA:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['pantalla']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"FALLAS:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['fallas_atender']), border=0, align= 'L')
              pdf.ln(th)
              pdf.set_font('Courier','B',12)
              pdf.cell(col_width*3,40,"COMPLETAS:", border=0, align= 'L')
              pdf.set_font('Courier','',12)
              pdf.cell(60,40, str(row['completas']), border=0, align= 'L')
              pdf.ln(th)
              i=i+1
              pdf.ln(th)

          pdf.ln(10)

          pdf.set_font('Times','',10.0)
          pdf.cell(page_width, 0.0, '- end of report -', align='C')

          return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=dimmes_reportes_personal.pdf'}) #reporte_dimme
          cursor.close()
          conn.commit()

#imprimir PDF
@app.route('/downloadi/reportd/pdfd')
def download_reportd():
          now=date.today()
          conn= mysql.connect()
          cursor= conn.cursor(pymysql.cursors.DictCursor)

          #cursor.execute("SELECT fotografia,nombre,num_empleado,unidad,num_dimme,nom_emergencia,num_emergencia,vigencia FROM info_tecnicos")
          cursor.execute("SELECT * FROM info_dimmes")
          result= cursor.fetchall()
          
          pdf = FPDF()
          pdf = FPDF('P', 'mm', (400, 300))
          pdf.add_page()

          page_width =pdf.w - 2 * pdf.l_margin

          page_width =pdf.w - 2 * pdf.l_margin
          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'MEGACABLE COMUNICACIONES S.A. DE C.V.', align='C')
          pdf.ln(8)

          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'---Atención Domiciliaria---', align='C')
          pdf.ln(4)

          absolutepath = os.path.abspath(__file__)
          fileDirectory = os.path.dirname(absolutepath)
          newPath2 = os.path.join(fileDirectory,'logo.jpg')   
          pdf.image(newPath2,x=12,y=8,w=45,h=35)
          pdf.ln(5)

          pdf.set_font('Times','B',12.0)
          pdf.cell(page_width,0.0,'Reporte: ', align='C')
          pdf.ln(6)

          pdf.set_font('Times','B',14.0)
          pdf.cell(page_width,0.0,'"INFORMACIÓN DE DIMMES"', align='C')
          pdf.ln(13)

          pdf.set_font('Times','B',12.0)
          pdf.cell(page_width,0.0,'Fecha: '+str(date.strftime("%d / %m / %y")), align='L')
          pdf.ln(5)
          
          pdf.set_font('Courier','B',12)
          #pdf.set_font('Courier','',12)

          col_width=page_width/9

          pdf.ln(1)

          
          th = pdf.font_size*2.4
          i=1
          pdf.cell(15, 10,"N°", border=1, align= 'C')
          pdf.cell(35, 10,"CUADRILLA", border=1, align= 'C')
          pdf.cell(25, 10,"ETIQUETA", border=1, align= 'C')
          pdf.cell(40, 10,"NUMERO", border=1, align= 'C')
          pdf.cell(50, 10,"IMEI 1", border=1, align= 'C')
          pdf.cell(30, 10,"MODELO", border=1, align= 'C')
          pdf.cell(50, 10,"SERIE", border=1, align= 'C')
          pdf.cell(55, 10,"IMEI SIM", border=1, align= 'C')
          pdf.cell(70, 10,"OBSERVACIONES", border=1, align= 'C')
          pdf.ln(th)
          for row in result:
              pdf.set_font('Courier','',12)
              #Bordes
              pdf.cell(15, 15, txt= str(i), border= 0,align= 'L')
              pdf.cell(35, 15, txt= str(row['cuadrilla']), border= 0, align= 'L')
              pdf.cell(25, 15, txt= row['etiqueta'], border= 0, align= 'L')
              pdf.cell(40, 15, txt= row['numero'], border= 0,align= 'L')
              pdf.cell(50, 15, txt= row['imei_1'], border= 0,align= 'L')
              pdf.cell(30, 15, txt= row['modelo'], border= 0,align= 'L')
              pdf.cell(50, 15, txt= row['serie'], border= 0,align= 'L') 
              pdf.cell(55, 15, txt= row['imei_sim'], border= 0,align= 'L')
              pdf.multi_cell(70, 5, row['observaciones'], border= 0, align= 'L')
              i=i+1
              pdf.ln(3)
          pdf.ln(10)

          pdf.set_font('Times','',10.0)
          pdf.cell(page_width, 0.0, '- end of report -', align='C')
          
          return Response(pdf.output(dest='S').encode('latin-1'), mimetype='applicationd/pdfd', headers={'Content-Disposition':'attachment;filename=dimmes_reporte.pdf'}) #reporte_dimmes

          cursor.close()
          conn.commit()

@app.route('/destroyid/<int:id>')
def destroyid(id):
    conn= mysql.connect()
    cursor= conn.cursor()

    cursor.execute("DELETE FROM info_dimmes WHERE id=%s", (id))
    conn.commit()
    return redirect('http://20.114.233.203/idimmes')

@app.route('/editid/<int:id>')
def editid(id):
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM info_dimmes WHERE id=%s", (id))
    infod=cursor.fetchall()   
    conn.commit()
    print(infod)
    
    return render_template('dimmes/editid.html',info_dimmes=infod)

@app.route('/datosd/<int:id>')
def datosd(id):
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM info_dimmes WHERE id=%s", (id))
    infod=cursor.fetchall()   
    conn.commit()
    print(infod)
    
    return render_template('dimmes/datosd.html',info_dimmes=infod)

@app.route('/updateid', methods=['POST'])
def updateid():
    _cuadrillad=request.form['txtCuadrillaD']
    _etiqueta=request.form['txtEtiqueta']
    _numerodi=request.form['txtNumeroDi']
    _imei1=request.form['txtImei1']
    _imei2=request.form['txtImei2']
    _modelo=request.form['txtModelo']
    _serie=request.form['txtSerie']
    _nombred=request.form['txtNombreD']
    _imeis=request.form['txtImeiS']
    _observaciones=request.form['txtObservaciones']
    _pantalla=request.form['txtPantalla']
    _fallas=request.form['txtFallas']
    _completas=request.form['txtCompletas']
    idd=request.form['txtIDd']
    
    
    sql="UPDATE info_dimmes SET cuadrilla=%s, etiqueta=%s, numero=%s, imei_1=%s, imei_2=%s, modelo=%s, serie=%s, nombre=%s, imei_sim=%s, observaciones=%s, pantalla=%s, fallas_atender=%s, completas=%s WHERE id=%s;"
    
    datosid=(_cuadrillad, _etiqueta, _numerodi, _imei1, _imei2, _modelo, _serie, _nombred, _imeis, _observaciones, _pantalla, _fallas, _completas, idd)
    
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datosid)
    conn.commit()
    
    return redirect('http://20.114.233.203/idimmes') 

#-----------------------HERRAMIENTAS_TECNICOS--------------------
#la aplicación recibira solicitudes mediante la URL (host)
@app.route('/herramientast')
def indexht():

    sql="SELECT * FROM `herramientas_tecnicos`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    
    infoh=cursor.fetchall()
    print(infoh)
    
    conn.commit()

    conn.close()
    sql="SELECT * FROM `info_tecnicos`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    infotec=cursor.fetchall()
    print(infotec)
    conn.commit()

    #accedera directamente a index.html | Enviar la información a la ventana de index 
    #return render_template('herramientas/indexht.html',herramientas_tecnicos=infoh)
    return render_template('herramientas/indexht.html',herramientas_tecnicos=infoh,info_tecnicos=infotec)
 
    
@app.route('/createht')
def createht():
    
    return render_template('herramientas/createht.html')

@app.route('/storeht', methods=['POST'])
def storageht():
    _herramienta=request.form['txtHerramienta']
    _numeroeh=request.form['txtNumeroEH']
    _enero=request.form['txtEnero']
    _febrero=request.form['txtFebrero']
    _marzo=request.form['txtMarzo']
    _abril=request.form['txtAbril']
    _mayo=request.form['txtMayo']
    _junio=request.form['txtJunio']
    _julio=request.form['txtJulio']
    _agosto=request.form['txtAgosto']
    _septiembre=request.form['txtSeptiembre']
    _octubre=request.form['txtOctubre']
    _noviembre=request.form['txtNoviembre']
    _diciembre=request.form['txtDiciembre']

    if _herramienta=='' or _numeroeh=='' or _enero=='' or _febrero=='' or _marzo=='' or _abril=='' or _mayo=='' or _junio=='' or _julio=='' or _agosto=='' or _septiembre=='' or _octubre=='' or _noviembre=='' or _diciembre=='':
        flash('Recuerda llenar todos los datos de los campos') 
        return redirect(url_for('createht'))   
    

    sql="INSERT INTO `herramientas_tecnicos` (`id`, `herramienta`, `num_empleado`, `enero`, `febrero`, `marzo`, `abril`, `mayo`, `junio`, `julio`, `agosto`, `septiembre`, `octubre`, `noviembre`, `diciembre`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    
    datosht=(_herramienta, _numeroeh, _enero, _febrero, _marzo, _abril, _mayo, _junio, _julio, _agosto, _septiembre, _octubre, _noviembre, _diciembre)
    
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datosht)
    conn.commit()
    
    #return render_template('vehiculos/indexit.html')
    return redirect('http://20.114.233.203/herramientast') 

@app.route('/destroyht/<int:id>')
def destroyht(id):
    conn= mysql.connect()
    cursor= conn.cursor()

    cursor.execute("DELETE FROM herramientas_tecnicos WHERE id=%s", (id))
    conn.commit()
    return redirect('http://20.114.233.203/herramientast')

@app.route('/editht/<int:id>')
def editht(id):
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM herramientas_tecnicos WHERE id=%s", (id))
    infoh=cursor.fetchall()   
    conn.commit()
    print(infoh)
    
    return render_template('herramientas/editht.html',herramientas_tecnicos=infoh)

@app.route('/updateht', methods=['POST'])
def updateht():
    _herramienta=request.form['txtHerramienta']
    _numeroeh=request.form['txtNumeroEH']
    _enero=request.form['txtEnero']
    _febrero=request.form['txtFebrero']
    _marzo=request.form['txtMarzo']
    _abril=request.form['txtAbril']
    _mayo=request.form['txtMayo']
    _junio=request.form['txtJunio']
    _julio=request.form['txtJulio']
    _agosto=request.form['txtAgosto']
    _septiembre=request.form['txtSeptiembre']
    _octubre=request.form['txtOctubre']
    _noviembre=request.form['txtNoviembre']
    _diciembre=request.form['txtDiciembre']
    idht=request.form['txtIDht'] 

    sql="UPDATE herramientas_tecnicos SET herramienta=%s, num_empleado=%s, enero=%s, febrero=%s, marzo=%s, abril=%s, mayo=%s, junio=%s, julio=%s, agosto=%s, septiembre=%s, octubre=%s, noviembre=%s, diciembre=%s WHERE id=%s;" 
    
    datosht=(_herramienta, _numeroeh, _enero, _febrero, _marzo, _abril, _mayo, _junio, _julio, _agosto, _septiembre, _octubre, _noviembre, _diciembre, idht)
    
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datosht)
    conn.commit()

    #return render_template('vehiculos/indexit.html')
    return redirect('http://20.114.233.203/herramientast')

@app.route('/datosh/<int:id>')
#def datosh(id):
#    conn= mysql.connect()
#    cursor= conn.cursor()
#    cursor.execute("SELECT * FROM herramientas_tecnicos WHERE id=%s", (id))
#    infoh=cursor.fetchall()   
#    conn.commit()
#    print(infoh)
    
#    return render_template('herramientas/datosh.html',herramientas_tecnicos=infoh)

def obtener_conexion():
    return pymysql.connect(host='localhost',user='root',password='',db='bdb1')

#imprimir PDF por registro
@app.route('/downloadh/reporth/pdfhtas',methods=['GET','POST'])
def downloaddd1_reportddd1():
    sid= request.form.get('sid')
    now=date.today()
   
   
    conexion = obtener_conexion()
    resultados = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM herramientas_tecnicos WHERE num_empleado=%s", sid)
        resultados = cursor.fetchall()
    
    now=date.today()
    print(id)
   
    pdf = FPDF()
    pdf = FPDF('P', 'mm', (380, 400))
    pdf.add_page()

    page_width =pdf.w - 2 * pdf.l_margin

    pdf.ln(8)
    pdf.set_font('Times','B',14.0)
    pdf.cell(page_width,0.0,'MEGACABLE COMUNICACIONES S.A. DE C.V.', align='C')
    pdf.ln(8)

    pdf.set_font('Times','B',14.0)
    pdf.cell(page_width,0.0,'---Atención Domiciliaria---', align='C')
    pdf.ln(4)

    absolutepath = os.path.abspath(__file__)
    fileDirectory = os.path.dirname(absolutepath)
    newPath2 = os.path.join(fileDirectory,'logo.jpg')   
    pdf.image(newPath2,x=12,y=8,w=45,h=35)
    pdf.ln(5)

    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,'Reporte: ', align='C')
    pdf.ln(6)

    pdf.set_font('Times','B',14.0)
    pdf.cell(page_width,0.0,'"INFORMACIÓN DE HERRAMIENTAS"', align='C')
    pdf.ln(13)

    pdf.set_font('Times','B',12.0)
    pdf.cell(page_width,0.0,'Fecha: '+str(date.strftime("%d / %m / %y")), align='L')
    pdf.ln(5)

    pdf.set_font('Courier','B',12)
    col_width=page_width/9

    pdf.ln(1)
    th = pdf.font_size*2.4
    i=1
    pdf.cell(15,10,"N°", border=1, align= 'C')
    pdf.cell(45,10,"HERRAMIENTA", border=1, align= 'C')
    pdf.cell(35,10,"N° EMPLEADO", border=1, align= 'C')
    pdf.cell(20,10,"ENE.", border=1, align= 'C')
    pdf.cell(20,10,"FEB.", border=1, align= 'C')
    pdf.cell(20,10,"MZO.", border=1, align= 'C')
    pdf.cell(20,10,"ABR.", border=1, align= 'C')
    pdf.cell(20,10,"MY.", border=1, align= 'C')
    pdf.cell(20,10,"JUN.", border=1, align= 'C')
    pdf.cell(20,10,"JUL.", border=1, align= 'C')
    pdf.cell(20,10,"AGT.", border=1, align= 'C')
    pdf.cell(20,10,"SEPT.", border=1, align= 'C')
    pdf.cell(20,10,"OCT.", border=1, align= 'C')
    pdf.cell(20,10,"NOV.", border=1, align= 'C')
    pdf.cell(20,10,"DIC.", border=1, align= 'C')
    pdf.ln(th)
    for row in resultados:
        pdf.set_font('Courier','',12)
        print(row)
        pdf.cell(15,th, str(row[0]), border=1, align= 'L')
        pdf.cell(45,th, str(row[1]), border=1, align= 'L')
        pdf.cell(35,th, str(row[2]), border=1, align= 'L')
        pdf.cell(20,th, str(row[3]), border=1, align= 'C')
        pdf.cell(20,th, str(row[4]), border=1, align= 'C')
        pdf.cell(20,th, str(row[5]), border=1, align= 'C')
        pdf.cell(20,th, str(row[6]), border=1, align= 'C')
        pdf.cell(20,th, str(row[7]), border=1, align= 'C')
        pdf.cell(20,th, str(row[8]), border=1, align= 'C')
        pdf.cell(20,th, str(row[9]), border=1, align= 'C')
        pdf.cell(20,th, str(row[10]), border=1, align= 'C')
        pdf.cell(20,th, str(row[11]), border=1, align= 'C')
        pdf.cell(20,th, str(row[12]), border=1, align= 'C')
        pdf.cell(20,th, str(row[13]), border=1, align= 'C')
        pdf.cell(20,th, str(row[14]), border=1, align= 'C')
        i=i+1
        pdf.ln(10)
    pdf.ln(10)

    pdf.set_font('Times','',10.0)
    pdf.ln(th)
    pdf.cell(page_width, 0.0, '- end of report -', align='C')

    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='applicationh/pdfh', headers={'Content-Disposition':'attachment;filename=herramientas.pdf'}) #reporte_herramientas
    cursor.close()
    conn.commit()


#Referencias para que la aplicación empiece a funcionar
if __name__== '__main__':
    app.run(debug=True)
