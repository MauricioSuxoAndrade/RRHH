from flask import Flask, render_template, request, redirect, url_for
from flask import send_file
from models import db, Usuario, Acceso, AFP, Asistencia, CajaSalud, Candidato, Capacitacion, Contrato, Departamento, Emplea, Empleado, EvaluacionDesempeno, Gestiona,  Historial, Informe, Notifica, Participa, Permiso, Posee, Postula, RegistroPago, Rol, Vacante
from datetime import date
import io


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://usuario:1234@localhost/p?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/usuarios')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        # Calcular el siguiente ID manualmente
        ultimo_usuario = Usuario.query.order_by(Usuario.id_usuario.desc()).first()
        nuevo_id = (ultimo_usuario.id_usuario + 1) if ultimo_usuario else 1

        # Crear un nuevo usuario
        nuevo_usuario = Usuario(
            id_usuario=nuevo_id,
            nombre_usuario=request.form['nombre_usuario'],
            correo=request.form['correo'],
            estado_usuario=request.form['estado_usuario'],
            contrasena=request.form['contrasena'],
            fecha_creacion=date.today()
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('listar_usuarios'))
    return render_template('usuarios/crear.html')

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nombre_usuario = request.form['nombre_usuario']
        usuario.correo = request.form['correo']
        usuario.estado_usuario = request.form['estado_usuario']
        usuario.contrasena = request.form['contrasena']
        # Nota: No modificamos `fecha_creacion`
        db.session.commit()
        return redirect(url_for('listar_usuarios'))
    return render_template('usuarios/editar.html', usuario=usuario)

@app.route('/usuarios/eliminar/<int:id>', methods=['GET'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id) 
    db.session.delete(usuario)  
    db.session.commit() 
    return redirect(url_for('listar_usuarios'))  


@app.route('/accesos')
def listar_accesos():
    accesos = Acceso.query.all()
    return render_template('accesos/listar.html', accesos=accesos)

@app.route('/accesos/crear', methods=['GET', 'POST'])
def crear_acceso():
    if request.method == 'POST':
        # Crear un nuevo acceso
        nuevo_acceso = Acceso(
            nombre_acceso=request.form['nombre_acceso'],
            descripcion_acceso=request.form['descripcion_acceso']
        )
        db.session.add(nuevo_acceso)
        db.session.commit()
        return redirect(url_for('listar_accesos'))
    return render_template('accesos/crear.html')

@app.route('/accesos/editar/<int:id>', methods=['GET', 'POST'])
def editar_acceso(id):
    acceso = Acceso.query.get_or_404(id)
    if request.method == 'POST':
        acceso.nombre_acceso = request.form['nombre_acceso']
        acceso.descripcion_acceso = request.form['descripcion_acceso']
        db.session.commit()
        return redirect(url_for('listar_accesos'))
    return render_template('accesos/editar.html', acceso=acceso)

@app.route('/accesos/eliminar/<int:id>', methods=['GET'])
def eliminar_acceso(id):
    acceso = Acceso.query.get_or_404(id)
    db.session.delete(acceso)
    db.session.commit()
    return redirect(url_for('listar_accesos'))


@app.route('/afps')
def listar_afps():
    afps = AFP.query.all()
    return render_template('afps/listar.html', afps=afps)

@app.route('/afps/crear', methods=['GET', 'POST'])
def crear_afp():
    if request.method == 'POST':
        nuevo_afp = AFP(
            nombre=request.form['nombre'],
            monto_apo=request.form['monto_apo']
        )
        db.session.add(nuevo_afp)
        db.session.commit()
        return redirect(url_for('listar_afps'))
    return render_template('afps/crear.html')

@app.route('/afps/editar/<int:id>', methods=['GET', 'POST'])
def editar_afp(id):
    afp = AFP.query.get_or_404(id)
    if request.method == 'POST':
        afp.nombre = request.form['nombre']
        afp.monto_apo = request.form['monto_apo']
        db.session.commit()
        return redirect(url_for('listar_afps'))
    return render_template('afps/editar.html', afp=afp)

@app.route('/afps/eliminar/<int:id>', methods=['GET'])
def eliminar_afp(id):
    afp = AFP.query.get_or_404(id)
    db.session.delete(afp)
    db.session.commit()
    return redirect(url_for('listar_afps'))

@app.route('/asistencias')
def listar_asistencias():
    asistencias = Asistencia.query.all()
    return render_template('asistencias/listar.html', asistencias=asistencias)

@app.route('/asistencias/crear', methods=['GET', 'POST'])
def crear_asistencia():
    if request.method == 'POST':
        nueva_asistencia = Asistencia(
            id_empleado=request.form['id_empleado'],
            fecha_asis=request.form['fecha_asis'],
            hora_ent=request.form['hora_ent'],
            hora_sal=request.form['hora_sal'],
            hora_extr=request.form['hora_extr']
        )
        db.session.add(nueva_asistencia)
        db.session.commit()
        return redirect(url_for('listar_asistencias'))
    return render_template('asistencias/crear.html')

@app.route('/asistencias/editar/<int:id>', methods=['GET', 'POST'])
def editar_asistencia(id):
    asistencia = Asistencia.query.get_or_404(id)
    if request.method == 'POST':
        asistencia.id_empleado = request.form['id_empleado']
        asistencia.fecha_asis = request.form['fecha_asis']
        asistencia.hora_ent = request.form['hora_ent']
        asistencia.hora_sal = request.form['hora_sal']
        asistencia.hora_extr = request.form['hora_extr']
        db.session.commit()
        return redirect(url_for('listar_asistencias'))
    return render_template('asistencias/editar.html', asistencia=asistencia)

@app.route('/asistencias/eliminar/<int:id>', methods=['GET'])
def eliminar_asistencia(id):
    asistencia = Asistencia.query.get_or_404(id)
    db.session.delete(asistencia)
    db.session.commit()
    return redirect(url_for('listar_asistencias'))

@app.route('/caja_salud')
def listar_caja_salud():
    cajas = CajaSalud.query.all()
    return render_template('caja_salud/listar.html', cajas=cajas)

@app.route('/caja_salud/crear', methods=['GET', 'POST'])
def crear_caja_salud():
    if request.method == 'POST':
        nueva_caja = CajaSalud(
            nombre_c=request.form['nombre_c'],
            monto_apo=request.form['monto_apo']
        )
        db.session.add(nueva_caja)
        db.session.commit()
        return redirect(url_for('listar_caja_salud'))
    return render_template('caja_salud/crear.html')

@app.route('/caja_salud/editar/<int:id>', methods=['GET', 'POST'])
def editar_caja_salud(id):
    caja = CajaSalud.query.get_or_404(id)
    if request.method == 'POST':
        caja.nombre_c = request.form['nombre_c']
        caja.monto_apo = request.form['monto_apo']
        db.session.commit()
        return redirect(url_for('listar_caja_salud'))
    return render_template('caja_salud/editar.html', caja=caja)

@app.route('/caja_salud/eliminar/<int:id>', methods=['GET'])
def eliminar_caja_salud(id):
    caja = CajaSalud.query.get_or_404(id)
    db.session.delete(caja)
    db.session.commit()
    return redirect(url_for('listar_caja_salud'))


@app.route('/candidatos')
def listar_candidatos():
    candidatos = Candidato.query.all()
    return render_template('candidatos/listar.html', candidatos=candidatos)

@app.route('/candidatos/crear', methods=['GET', 'POST'])
def crear_candidato():
    if request.method == 'POST':
        foto = request.files['foto']
        nueva_candidato = Candidato(
            id_departamento=request.form['id_departamento'],
            nombre=request.form['nombre'],
            ap_paterno=request.form['ap_paterno'],
            ap_materno=request.form['ap_materno'],
            fec_nac=request.form['fec_nac'],
            telefono=request.form['telefono'],
            foto=foto.read() if foto else None
        )
        db.session.add(nueva_candidato)
        db.session.commit()
        return redirect(url_for('listar_candidatos'))
    return render_template('candidatos/crear.html')

@app.route('/candidatos/editar/<int:id>', methods=['GET', 'POST'])
def editar_candidato(id):
    candidato = Candidato.query.get_or_404(id)
    if request.method == 'POST':
        foto = request.files['foto']
        candidato.id_departamento = request.form['id_departamento']
        candidato.nombre = request.form['nombre']
        candidato.ap_paterno = request.form['ap_paterno']
        candidato.ap_materno = request.form['ap_materno']
        candidato.fec_nac = request.form['fec_nac']
        candidato.telefono = request.form['telefono']
        if foto:
            candidato.foto = foto.read()
        db.session.commit()
        return redirect(url_for('listar_candidatos'))
    return render_template('candidatos/editar.html', candidato=candidato)

@app.route('/candidatos/eliminar/<int:id>', methods=['GET'])
def eliminar_candidato(id):
    candidato = Candidato.query.get_or_404(id)
    db.session.delete(candidato)
    db.session.commit()
    return redirect(url_for('listar_candidatos'))

@app.route('/candidatos/foto/<int:id>')
def mostrar_foto(id):
    candidato = Candidato.query.get_or_404(id)
    if candidato.foto:
        return send_file(
            io.BytesIO(candidato.foto),
            mimetype='image/jpeg',
            as_attachment=False,
            download_name=f"foto_candidato_{id}.jpg"
        )
    return "Sin foto"

@app.route('/capacitaciones')
def listar_capacitaciones():
    capacitaciones = Capacitacion.query.all()
    return render_template('capacitaciones/listar.html', capacitaciones=capacitaciones)

@app.route('/capacitaciones/crear', methods=['GET', 'POST'])
def crear_capacitacion():
    if request.method == 'POST':
        nueva_capacitacion = Capacitacion(
            id_empleado=request.form['id_empleado'],
            nombre=request.form['nombre'],
            fecha_ini=request.form['fecha_ini'],
            fecha_fin=request.form['fecha_fin'],
            descripcion=request.form['descripcion']
        )
        db.session.add(nueva_capacitacion)
        db.session.commit()
        return redirect(url_for('listar_capacitaciones'))
    return render_template('capacitaciones/crear.html')

@app.route('/capacitaciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_capacitacion(id):
    capacitacion = Capacitacion.query.get_or_404(id)
    if request.method == 'POST':
        capacitacion.id_empleado = request.form['id_empleado']
        capacitacion.nombre = request.form['nombre']
        capacitacion.fecha_ini = request.form['fecha_ini']
        capacitacion.fecha_fin = request.form['fecha_fin']
        capacitacion.descripcion = request.form['descripcion']
        db.session.commit()
        return redirect(url_for('listar_capacitaciones'))
    return render_template('capacitaciones/editar.html', capacitacion=capacitacion)

@app.route('/capacitaciones/eliminar/<int:id>', methods=['GET'])
def eliminar_capacitacion(id):
    capacitacion = Capacitacion.query.get_or_404(id)
    db.session.delete(capacitacion)
    db.session.commit()
    return redirect(url_for('listar_capacitaciones'))

@app.route('/contratos')
def listar_contratos():
    contratos = Contrato.query.all()
    return render_template('contratos/listar.html', contratos=contratos)

@app.route('/contratos/crear', methods=['GET', 'POST'])
def crear_contrato():
    if request.method == 'POST':
        nuevo_contrato = Contrato(
            id_empleado=request.form['id_empleado'],
            tipo_cont=request.form['tipo_cont'],
            fec_ini=request.form['fec_ini'],
            fec_fin=request.form['fec_fin'],
            condiciones=request.form['condiciones'],
            salario=request.form['salario']
        )
        db.session.add(nuevo_contrato)
        db.session.commit()
        return redirect(url_for('listar_contratos'))
    return render_template('contratos/crear.html')

@app.route('/contratos/editar/<int:id>', methods=['GET', 'POST'])
def editar_contrato(id):
    contrato = Contrato.query.get_or_404(id)
    if request.method == 'POST':
        contrato.id_empleado = request.form['id_empleado']
        contrato.tipo_cont = request.form['tipo_cont']
        contrato.fec_ini = request.form['fec_ini']
        contrato.fec_fin = request.form['fec_fin']
        contrato.condiciones = request.form['condiciones']
        contrato.salario = request.form['salario']
        db.session.commit()
        return redirect(url_for('listar_contratos'))
    return render_template('contratos/editar.html', contrato=contrato)

@app.route('/contratos/eliminar/<int:id>', methods=['GET'])
def eliminar_contrato(id):
    contrato = Contrato.query.get_or_404(id)
    db.session.delete(contrato)
    db.session.commit()
    return redirect(url_for('listar_contratos'))

@app.route('/departamentos')
def listar_departamentos():
    departamentos = Departamento.query.all()
    return render_template('departamentos/listar.html', departamentos=departamentos)

@app.route('/departamentos/crear', methods=['GET', 'POST'])
def crear_departamento():
    if request.method == 'POST':
        nuevo_departamento = Departamento(
            id_jefe=request.form['id_jefe'],
            nom_departamento=request.form['nom_departamento'],
            descripcion=request.form['descripcion']
        )
        db.session.add(nuevo_departamento)
        db.session.commit()
        return redirect(url_for('listar_departamentos'))
    return render_template('departamentos/crear.html')

@app.route('/departamentos/editar/<int:id>', methods=['GET', 'POST'])
def editar_departamento(id):
    departamento = Departamento.query.get_or_404(id)
    if request.method == 'POST':
        departamento.id_jefe = request.form['id_jefe']
        departamento.nom_departamento = request.form['nom_departamento']
        departamento.descripcion = request.form['descripcion']
        db.session.commit()
        return redirect(url_for('listar_departamentos'))
    return render_template('departamentos/editar.html', departamento=departamento)

@app.route('/departamentos/eliminar/<int:id>', methods=['GET'])
def eliminar_departamento(id):
    departamento = Departamento.query.get_or_404(id)
    db.session.delete(departamento)
    db.session.commit()
    return redirect(url_for('listar_departamentos'))

@app.route('/emplea')
def listar_emplea():
    emplea = Emplea.query.all()
    return render_template('emplea/listar.html', emplea=emplea)

@app.route('/emplea/crear', methods=['GET', 'POST'])
def crear_emplea():
    if request.method == 'POST':
        nuevo_emplea = Emplea(
            id_acceso=request.form['id_acceso'],
            id_rol=request.form['id_rol']
        )
        db.session.add(nuevo_emplea)
        db.session.commit()
        return redirect(url_for('listar_emplea'))
    return render_template('emplea/crear.html')

@app.route('/emplea/eliminar/<int:id_acceso>/<int:id_rol>', methods=['GET'])
def eliminar_emplea(id_acceso, id_rol):
    emplea = Emplea.query.filter_by(id_acceso=id_acceso, id_rol=id_rol).first_or_404()
    db.session.delete(emplea)
    db.session.commit()
    return redirect(url_for('listar_emplea'))

@app.route('/emplea/editar/<int:id_acceso>/<int:id_rol>', methods=['GET', 'POST'])
def editar_emplea(id_acceso, id_rol):
    # Busca la relación existente
    emplea = Emplea.query.filter_by(id_acceso=id_acceso, id_rol=id_rol).first_or_404()

    if request.method == 'POST':
        # Obtén los nuevos valores del formulario
        nuevo_id_acceso = request.form['id_acceso']
        nuevo_id_rol = request.form['id_rol']

        # Verifica si la nueva relación ya existe para evitar duplicados
        if Emplea.query.filter_by(id_acceso=nuevo_id_acceso, id_rol=nuevo_id_rol).first():
            return "Error: La relación con esos valores ya existe.", 400

        # Actualiza los valores de la relación
        emplea.id_acceso = nuevo_id_acceso
        emplea.id_rol = nuevo_id_rol

        # Guarda los cambios en la base de datos
        db.session.commit()
        return redirect(url_for('listar_emplea'))

    # Muestra la plantilla con los valores actuales
    return render_template('emplea/editar.html', emplea=emplea)

@app.route('/empleados')
def listar_empleados():
    empleados = Empleado.query.all()
    return render_template('empleados/listar.html', empleados=empleados)

@app.route('/empleados/crear', methods=['GET', 'POST'])
def crear_empleado():
    if request.method == 'POST':
        foto = request.files['foto']
        nuevo_empleado = Empleado(
            id_usuario=request.form['id_usuario'],
            id_departamento_pertenece=request.form['id_departamento_pertenece'],
            nombre=request.form['nombre'],
            ap_paterno=request.form['ap_paterno'],
            ap_materno=request.form['ap_materno'],
            fec_nac=request.form['fec_nac'],
            foto=foto.read() if foto else None,
            direccion=request.form['direccion'],
            cargo=request.form['cargo'],
            est_emp=request.form['est_emp']
        )
        db.session.add(nuevo_empleado)
        db.session.commit()
        return redirect(url_for('listar_empleados'))
    return render_template('empleados/crear.html')



@app.route('/empleados/eliminar/<int:id>', methods=['GET'])
def eliminar_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    db.session.delete(empleado)
    db.session.commit()
    return redirect(url_for('listar_empleados'))

@app.route('/empleados/foto/<int:id>')
def mostrar_foto_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    if empleado.foto:
        return send_file(
            io.BytesIO(empleado.foto),
            mimetype='image/jpeg',
            as_attachment=False,
            download_name=f"foto_empleado_{id}.jpg"
        )
    return "Sin foto"

@app.route('/empleados/editar/<int:id>', methods=['GET', 'POST'])
def editar_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    if request.method == 'POST':
        # Actualiza los campos del empleado con los datos del formulario
        empleado.id_usuario = request.form['id_usuario']
        empleado.id_departamento_pertenece = request.form['id_departamento_pertenece']
        empleado.nombre = request.form['nombre']
        empleado.ap_paterno = request.form['ap_paterno']
        empleado.ap_materno = request.form['ap_materno']
        empleado.fec_nac = request.form['fec_nac']
        empleado.direccion = request.form['direccion']
        empleado.cargo = request.form['cargo']
        empleado.est_emp = request.form['est_emp']

        # Manejo de foto
        foto = request.files['foto']
        if foto:  # Si se cargó una nueva foto
            empleado.foto = foto.read()

        # Guarda los cambios
        db.session.commit()
        return redirect(url_for('listar_empleados'))

    return render_template('empleados/editar.html', empleado=empleado)

@app.route('/evaluaciones')
def listar_evaluaciones():
    evaluaciones = EvaluacionDesempeno.query.all()
    return render_template('evaluaciones/listar.html', evaluaciones=evaluaciones)

@app.route('/evaluaciones/crear', methods=['GET', 'POST'])
def crear_evaluacion():
    if request.method == 'POST':
        nueva_evaluacion = EvaluacionDesempeno(
            id_candidato=request.form['id_candidato'],
            id_empleado_realiza=request.form['id_empleado_realiza'],
            id_empleado_genera=request.form['id_empleado_genera'],
            fecha_evaluacion=request.form['fecha_evaluacion'],
            puntuacion=request.form['puntuacion'],
            comentario=request.form['comentario']
        )
        db.session.add(nueva_evaluacion)
        db.session.commit()
        return redirect(url_for('listar_evaluaciones'))
    return render_template('evaluaciones/crear.html')

@app.route('/evaluaciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_evaluacion(id):
    evaluacion = EvaluacionDesempeno.query.get_or_404(id)
    if request.method == 'POST':
        evaluacion.id_candidato = request.form['id_candidato']
        evaluacion.id_empleado_realiza = request.form['id_empleado_realiza']
        evaluacion.id_empleado_genera = request.form['id_empleado_genera']
        evaluacion.fecha_evaluacion = request.form['fecha_evaluacion']
        evaluacion.puntuacion = request.form['puntuacion']
        evaluacion.comentario = request.form['comentario']
        db.session.commit()
        return redirect(url_for('listar_evaluaciones'))
    return render_template('evaluaciones/editar.html', evaluacion=evaluacion)

@app.route('/evaluaciones/eliminar/<int:id>', methods=['GET'])
def eliminar_evaluacion(id):
    evaluacion = EvaluacionDesempeno.query.get_or_404(id)
    db.session.delete(evaluacion)
    db.session.commit()
    return redirect(url_for('listar_evaluaciones'))

@app.route('/gestiona')
def listar_gestiona():
    gestiona = Gestiona.query.all()
    return render_template('gestiona/listar.html', gestiona=gestiona)

@app.route('/gestiona/crear', methods=['GET', 'POST'])
def crear_gestiona():
    if request.method == 'POST':
        nueva_gestion = Gestiona(
            id_rol=request.form['id_rol'],
            id_usuario=request.form['id_usuario']
        )
        # Verificar si la relación ya existe
        if Gestiona.query.filter_by(id_rol=nueva_gestion.id_rol, id_usuario=nueva_gestion.id_usuario).first():
            return "Error: La relación ya existe.", 400
        db.session.add(nueva_gestion)
        db.session.commit()
        return redirect(url_for('listar_gestiona'))
    return render_template('gestiona/crear.html')

@app.route('/gestiona/eliminar/<int:id_rol>/<int:id_usuario>', methods=['GET'])
def eliminar_gestiona(id_rol, id_usuario):
    gestion = Gestiona.query.filter_by(id_rol=id_rol, id_usuario=id_usuario).first_or_404()
    db.session.delete(gestion)
    db.session.commit()
    return redirect(url_for('listar_gestiona'))

@app.route('/gestiona/editar/<int:id_rol>/<int:id_usuario>', methods=['GET', 'POST'])
def editar_gestiona(id_rol, id_usuario):
    gestion = Gestiona.query.filter_by(id_rol=id_rol, id_usuario=id_usuario).first_or_404()
    if request.method == 'POST':
        nuevo_id_rol = request.form['id_rol']
        nuevo_id_usuario = request.form['id_usuario']

        # Verificar si la nueva relación ya existe
        if Gestiona.query.filter_by(id_rol=nuevo_id_rol, id_usuario=nuevo_id_usuario).first():
            return "Error: La nueva relación ya existe.", 400

        gestion.id_rol = nuevo_id_rol
        gestion.id_usuario = nuevo_id_usuario
        db.session.commit()
        return redirect(url_for('listar_gestiona'))
    return render_template('gestiona/editar.html', gestion=gestion)

@app.route('/historial')
def listar_historial():
    historial = Historial.query.all()
    return render_template('historial/listar.html', historial=historial)

@app.route('/historial/crear', methods=['GET', 'POST'])
def crear_historial():
    if request.method == 'POST':
        nuevo_historial = Historial(
            id_empleado=request.form['id_empleado'],
            fecha_cambio=request.form['fecha_cambio'],
            tipo_cambio=request.form['tipo_cambio'],
            det_cambio=request.form['det_cambio'],
            mot_cambio=request.form['mot_cambio']
        )
        db.session.add(nuevo_historial)
        db.session.commit()
        return redirect(url_for('listar_historial'))
    return render_template('historial/crear.html')

@app.route('/historial/editar/<int:id>', methods=['GET', 'POST'])
def editar_historial(id):
    historial = Historial.query.get_or_404(id)
    if request.method == 'POST':
        historial.id_empleado = request.form['id_empleado']
        historial.fecha_cambio = request.form['fecha_cambio']
        historial.tipo_cambio = request.form['tipo_cambio']
        historial.det_cambio = request.form['det_cambio']
        historial.mot_cambio = request.form['mot_cambio']
        db.session.commit()
        return redirect(url_for('listar_historial'))
    return render_template('historial/editar.html', historial=historial)

@app.route('/historial/eliminar/<int:id>', methods=['GET'])
def eliminar_historial(id):
    historial = Historial.query.get_or_404(id)
    db.session.delete(historial)
    db.session.commit()
    return redirect(url_for('listar_historial'))

@app.route('/informes')
def listar_informes():
    informes = Informe.query.all()
    return render_template('informes/listar.html', informes=informes)

@app.route('/informes/crear', methods=['GET', 'POST'])
def crear_informe():
    if request.method == 'POST':
        nuevo_informe = Informe(
            id_empleado=request.form['id_empleado'],
            fecha_informe=request.form['fecha_informe'],
            estado_informe=request.form['estado_informe'],
            tipo_informe=request.form['tipo_informe'],
            criterio_busqueda=request.form['criterio_busqueda']
        )
        db.session.add(nuevo_informe)
        db.session.commit()
        return redirect(url_for('listar_informes'))
    return render_template('informes/crear.html')

@app.route('/informes/editar/<int:id>', methods=['GET', 'POST'])
def editar_informe(id):
    informe = Informe.query.get_or_404(id)
    if request.method == 'POST':
        informe.id_empleado = request.form['id_empleado']
        informe.fecha_informe = request.form['fecha_informe']
        informe.estado_informe = request.form['estado_informe']
        informe.tipo_informe = request.form['tipo_informe']
        informe.criterio_busqueda = request.form['criterio_busqueda']
        db.session.commit()
        return redirect(url_for('listar_informes'))
    return render_template('informes/editar.html', informe=informe)

@app.route('/informes/eliminar/<int:id>', methods=['GET'])
def eliminar_informe(id):
    informe = Informe.query.get_or_404(id)
    db.session.delete(informe)
    db.session.commit()
    return redirect(url_for('listar_informes'))

@app.route('/notificaciones')
def listar_notificaciones():
    notificaciones = Notifica.query.all()
    return render_template('notifica/listar.html', notificaciones=notificaciones)

@app.route('/notificaciones/crear', methods=['GET', 'POST'])
def crear_notificacion():
    if request.method == 'POST':
        nueva_notificacion = Notifica(
            id_usuario_envia=request.form['id_usuario_envia'],
            id_usuario_recibe=request.form['id_usuario_recibe'],
            fecha_notificacion=request.form['fecha_notificacion']
        )
        # Verificar si la relación ya existe
        if Notifica.query.filter_by(
            id_usuario_envia=nueva_notificacion.id_usuario_envia,
            id_usuario_recibe=nueva_notificacion.id_usuario_recibe,
            fecha_notificacion=nueva_notificacion.fecha_notificacion
        ).first():
            return "Error: La notificación ya existe.", 400
        db.session.add(nueva_notificacion)
        db.session.commit()
        return redirect(url_for('listar_notificaciones'))
    return render_template('notifica/crear.html')

@app.route('/notificaciones/editar/<int:id_usuario_envia>/<int:id_usuario_recibe>', methods=['GET', 'POST'])
def editar_notificacion(id_usuario_envia, id_usuario_recibe):
    notificacion = Notifica.query.filter_by(id_usuario_envia=id_usuario_envia, id_usuario_recibe=id_usuario_recibe).first_or_404()
    if request.method == 'POST':
        notificacion.id_usuario_envia = request.form['id_usuario_envia']
        notificacion.id_usuario_recibe = request.form['id_usuario_recibe']
        notificacion.fecha_notificacion = request.form['fecha_notificacion']
        db.session.commit()
        return redirect(url_for('listar_notificaciones'))
    return render_template('notifica/editar.html', notificacion=notificacion)

@app.route('/notificaciones/eliminar/<int:id_usuario_envia>/<int:id_usuario_recibe>', methods=['GET'])
def eliminar_notificacion(id_usuario_envia, id_usuario_recibe):
    notificacion = Notifica.query.filter_by(id_usuario_envia=id_usuario_envia, id_usuario_recibe=id_usuario_recibe).first_or_404()
    db.session.delete(notificacion)
    db.session.commit()
    return redirect(url_for('listar_notificaciones'))

@app.route('/participaciones')
def listar_participaciones():
    participaciones = Participa.query.all()
    return render_template('participa/listar.html', participaciones=participaciones)

@app.route('/participaciones/crear', methods=['GET', 'POST'])
def crear_participacion():
    if request.method == 'POST':
        nueva_participacion = Participa(
            id_empleado=request.form['id_empleado'],
            id_capacitacion=request.form['id_capacitacion']
        )
        # Verificar si la relación ya existe
        if Participa.query.filter_by(id_empleado=nueva_participacion.id_empleado, id_capacitacion=nueva_participacion.id_capacitacion).first():
            return "Error: La participación ya existe.", 400
        db.session.add(nueva_participacion)
        db.session.commit()
        return redirect(url_for('listar_participaciones'))
    return render_template('participa/crear.html')

@app.route('/participaciones/eliminar/<int:id_empleado>/<int:id_capacitacion>', methods=['GET'])
def eliminar_participacion(id_empleado, id_capacitacion):
    participacion = Participa.query.filter_by(id_empleado=id_empleado, id_capacitacion=id_capacitacion).first_or_404()
    db.session.delete(participacion)
    db.session.commit()
    return redirect(url_for('listar_participaciones'))

@app.route('/participaciones/editar/<int:id_empleado>/<int:id_capacitacion>', methods=['GET', 'POST'])
def editar_participacion(id_empleado, id_capacitacion):
    participacion = Participa.query.filter_by(id_empleado=id_empleado, id_capacitacion=id_capacitacion).first_or_404()
    if request.method == 'POST':
        nuevo_id_empleado = request.form['id_empleado']
        nuevo_id_capacitacion = request.form['id_capacitacion']

        # Verificar si la nueva relación ya existe
        if Participa.query.filter_by(id_empleado=nuevo_id_empleado, id_capacitacion=nuevo_id_capacitacion).first():
            return "Error: La participación ya existe.", 400

        participacion.id_empleado = nuevo_id_empleado
        participacion.id_capacitacion = nuevo_id_capacitacion
        db.session.commit()
        return redirect(url_for('listar_participaciones'))
    return render_template('participa/editar.html', participacion=participacion)

@app.route('/permisos')
def listar_permisos():
    permisos = Permiso.query.all()
    return render_template('permisos/listar.html', permisos=permisos)

@app.route('/permisos/crear', methods=['GET', 'POST'])
def crear_permiso():
    if request.method == 'POST':
        nuevo_permiso = Permiso(
            id_empleado_aprobador=request.form['id_empleado_aprobador'],
            id_empleado_solicitante=request.form['id_empleado_solicitante'],
            tipo_permiso=request.form['tipo_permiso'],
            fecha_solicitud=request.form['fecha_solicitud'],
            fecha_aprobacion=request.form['fecha_aprobacion'],
            estado=request.form['estado']
        )
        db.session.add(nuevo_permiso)
        db.session.commit()
        return redirect(url_for('listar_permisos'))
    return render_template('permisos/crear.html')

@app.route('/permisos/editar/<int:id>', methods=['GET', 'POST'])
def editar_permiso(id):
    permiso = Permiso.query.get_or_404(id)
    if request.method == 'POST':
        permiso.id_empleado_aprobador = request.form['id_empleado_aprobador']
        permiso.id_empleado_solicitante = request.form['id_empleado_solicitante']
        permiso.tipo_permiso = request.form['tipo_permiso']
        permiso.fecha_solicitud = request.form['fecha_solicitud']
        permiso.fecha_aprobacion = request.form['fecha_aprobacion']
        permiso.estado = request.form['estado']
        db.session.commit()
        return redirect(url_for('listar_permisos'))
    return render_template('permisos/editar.html', permiso=permiso)

@app.route('/permisos/eliminar/<int:id>', methods=['GET'])
def eliminar_permiso(id):
    permiso = Permiso.query.get_or_404(id)
    db.session.delete(permiso)
    db.session.commit()
    return redirect(url_for('listar_permisos'))

@app.route('/posee')
def listar_posee():
    relaciones = Posee.query.all()
    return render_template('posee/listar.html', relaciones=relaciones)

@app.route('/posee/crear', methods=['GET', 'POST'])
def crear_posee():
    if request.method == 'POST':
        nueva_relacion = Posee(
            id_rol=request.form['id_rol'],
            id_usuario=request.form['id_usuario']
        )
        # Verificar si la relación ya existe
        if Posee.query.filter_by(id_rol=nueva_relacion.id_rol, id_usuario=nueva_relacion.id_usuario).first():
            return "Error: La relación ya existe.", 400
        db.session.add(nueva_relacion)
        db.session.commit()
        return redirect(url_for('listar_posee'))
    return render_template('posee/crear.html')

@app.route('/posee/editar/<int:id_rol>/<int:id_usuario>', methods=['GET', 'POST'])
def editar_posee(id_rol, id_usuario):
    relacion = Posee.query.filter_by(id_rol=id_rol, id_usuario=id_usuario).first_or_404()
    if request.method == 'POST':
        nueva_id_rol = request.form['id_rol']
        nueva_id_usuario = request.form['id_usuario']

        # Verificar si la nueva relación ya existe
        if Posee.query.filter_by(id_rol=nueva_id_rol, id_usuario=nueva_id_usuario).first():
            return "Error: La relación ya existe.", 400

        relacion.id_rol = nueva_id_rol
        relacion.id_usuario = nueva_id_usuario
        db.session.commit()
        return redirect(url_for('listar_posee'))
    return render_template('posee/editar.html', relacion=relacion)

@app.route('/posee/eliminar/<int:id_rol>/<int:id_usuario>', methods=['GET'])
def eliminar_posee(id_rol, id_usuario):
    relacion = Posee.query.filter_by(id_rol=id_rol, id_usuario=id_usuario).first_or_404()
    db.session.delete(relacion)
    db.session.commit()
    return redirect(url_for('listar_posee'))

@app.route('/postulaciones')
def listar_postulaciones():
    postulaciones = Postula.query.all()
    return render_template('postula/listar.html', postulaciones=postulaciones)

@app.route('/postulaciones/crear', methods=['GET', 'POST'])
def crear_postulacion():
    if request.method == 'POST':
        nueva_postulacion = Postula(
            id_vacante=request.form['id_vacante'],
            id_candidato=request.form['id_candidato']
        )
        # Verificar si la relación ya existe
        if Postula.query.filter_by(id_vacante=nueva_postulacion.id_vacante, id_candidato=nueva_postulacion.id_candidato).first():
            return "Error: La postulación ya existe.", 400
        db.session.add(nueva_postulacion)
        db.session.commit()
        return redirect(url_for('listar_postulaciones'))
    return render_template('postula/crear.html')

@app.route('/postulaciones/editar/<int:id_vacante>/<int:id_candidato>', methods=['GET', 'POST'])
def editar_postulacion(id_vacante, id_candidato):
    postulacion = Postula.query.filter_by(id_vacante=id_vacante, id_candidato=id_candidato).first_or_404()
    if request.method == 'POST':
        nueva_id_vacante = request.form['id_vacante']
        nueva_id_candidato = request.form['id_candidato']

        # Verificar si la nueva relación ya existe
        if Postula.query.filter_by(id_vacante=nueva_id_vacante, id_candidato=nueva_id_candidato).first():
            return "Error: La postulación ya existe.", 400

        postulacion.id_vacante = nueva_id_vacante
        postulacion.id_candidato = nueva_id_candidato
        db.session.commit()
        return redirect(url_for('listar_postulaciones'))
    return render_template('postula/editar.html', postulacion=postulacion)

@app.route('/postulaciones/eliminar/<int:id_vacante>/<int:id_candidato>', methods=['GET'])
def eliminar_postulacion(id_vacante, id_candidato):
    postulacion = Postula.query.filter_by(id_vacante=id_vacante, id_candidato=id_candidato).first_or_404()
    db.session.delete(postulacion)
    db.session.commit()
    return redirect(url_for('listar_postulaciones'))

@app.route('/registros_pago')
def listar_registros_pago():
    registros = RegistroPago.query.all()
    return render_template('registro_pago/listar.html', registros=registros)

@app.route('/registros_pago/crear', methods=['GET', 'POST'])
def crear_registro_pago():
    if request.method == 'POST':
        nuevo_registro = RegistroPago(
            id_empleado=request.form['id_empleado'],
            id_caja=request.form['id_caja'],
            id_afp=request.form['id_afp'],
            fecha_gen=request.form['fecha_gen'],
            sueldo_base=request.form['sueldo_base'],
            deducciones=request.form['deducciones'],
            bonificaciones=request.form['bonificaciones']
        )
        db.session.add(nuevo_registro)
        db.session.commit()
        return redirect(url_for('listar_registros_pago'))
    return render_template('registro_pago/crear.html')

@app.route('/registros_pago/editar/<int:id>', methods=['GET', 'POST'])
def editar_registro_pago(id):
    registro = RegistroPago.query.get_or_404(id)
    if request.method == 'POST':
        registro.id_empleado = request.form['id_empleado']
        registro.id_caja = request.form['id_caja']
        registro.id_afp = request.form['id_afp']
        registro.fecha_gen = request.form['fecha_gen']
        registro.sueldo_base = request.form['sueldo_base']
        registro.deducciones = request.form['deducciones']
        registro.bonificaciones = request.form['bonificaciones']
        db.session.commit()
        return redirect(url_for('listar_registros_pago'))
    return render_template('registro_pago/editar.html', registro=registro)

@app.route('/registros_pago/eliminar/<int:id>', methods=['GET'])
def eliminar_registro_pago(id):
    registro = RegistroPago.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    return redirect(url_for('listar_registros_pago'))

@app.route('/roles')
def listar_roles():
    roles = Rol.query.all()
    return render_template('roles/listar.html', roles=roles)

@app.route('/roles/crear', methods=['GET', 'POST'])
def crear_rol():
    if request.method == 'POST':
        nuevo_rol = Rol(
            nombre_rol=request.form['nombre_rol'],
            descripcion_rol=request.form['descripcion_rol']
        )
        db.session.add(nuevo_rol)
        db.session.commit()
        return redirect(url_for('listar_roles'))
    return render_template('roles/crear.html')

@app.route('/roles/editar/<int:id>', methods=['GET', 'POST'])
def editar_rol(id):
    rol = Rol.query.get_or_404(id)
    if request.method == 'POST':
        rol.nombre_rol = request.form['nombre_rol']
        rol.descripcion_rol = request.form['descripcion_rol']
        db.session.commit()
        return redirect(url_for('listar_roles'))
    return render_template('roles/editar.html', rol=rol)

@app.route('/roles/eliminar/<int:id>', methods=['GET'])
def eliminar_rol(id):
    rol = Rol.query.get_or_404(id)
    db.session.delete(rol)
    db.session.commit()
    return redirect(url_for('listar_roles'))

@app.route('/vacantes')
def listar_vacantes():
    vacantes = Vacante.query.all()
    return render_template('vacantes/listar.html', vacantes=vacantes)

@app.route('/vacantes/crear', methods=['GET', 'POST'])
def crear_vacante():
    if request.method == 'POST':
        nueva_vacante = Vacante(
            id_departamento=request.form['id_departamento'],
            titulo=request.form['titulo'],
            descripcion=request.form['descripcion'],
            fec_publi=request.form['fec_publi']
        )
        db.session.add(nueva_vacante)
        db.session.commit()
        return redirect(url_for('listar_vacantes'))
    return render_template('vacantes/crear.html')

@app.route('/vacantes/editar/<int:id>', methods=['GET', 'POST'])
def editar_vacante(id):
    vacante = Vacante.query.get_or_404(id)
    if request.method == 'POST':
        vacante.id_departamento = request.form['id_departamento']
        vacante.titulo = request.form['titulo']
        vacante.descripcion = request.form['descripcion']
        vacante.fec_publi = request.form['fec_publi']
        db.session.commit()
        return redirect(url_for('listar_vacantes'))
    return render_template('vacantes/editar.html', vacante=vacante)

@app.route('/vacantes/eliminar/<int:id>', methods=['GET'])
def eliminar_vacante(id):
    vacante = Vacante.query.get_or_404(id)
    db.session.delete(vacante)
    db.session.commit()
    return redirect(url_for('listar_vacantes'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
