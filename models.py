from flask_sqlalchemy import SQLAlchemy

# Crear la instancia global de SQLAlchemy
db = SQLAlchemy()



class Usuario(db.Model):
    __tablename__ = 'USUARIO'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    estado_usuario = db.Column(db.String(20))
    contrasena = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.Date)

class Acceso(db.Model):
    __tablename__ = 'ACCESO'
    id_acceso = db.Column(db.Integer, primary_key=True)
    nombre_acceso = db.Column(db.String(50), nullable=False)
    descripcion_acceso = db.Column(db.String(255))

class AFP(db.Model):
    __tablename__ = 'AFP'
    id_afp = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    monto_apo = db.Column(db.Integer)

class Asistencia(db.Model):
    __tablename__ = 'ASISTENCIA'
    id_asistencia = db.Column(db.Integer, primary_key=True)
    id_empleado = db.Column(db.Integer, nullable=False)  
    fecha_asis = db.Column(db.Date, nullable=False)
    hora_ent = db.Column(db.Date)
    hora_sal = db.Column(db.Date)
    hora_extr = db.Column(db.Date)

class CajaSalud(db.Model):
    __tablename__ = 'CAJA_SALUD'
    id_caja = db.Column(db.Integer, primary_key=True)
    nombre_c = db.Column(db.String(100), nullable=False)
    monto_apo = db.Column(db.Integer)

class Candidato(db.Model):
    __tablename__ = 'CANDIDATO'
    id_candidato = db.Column(db.Integer, primary_key=True)
    id_departamento = db.Column(db.Integer, nullable=False)  # Relación con DEPARTAMENTO
    nombre = db.Column(db.String(50), nullable=False)
    ap_paterno = db.Column(db.String(50), nullable=False)
    ap_materno = db.Column(db.String(50))
    fec_nac = db.Column(db.Date)
    telefono = db.Column(db.String(20))
    foto = db.Column(db.LargeBinary)  # Para almacenar fotos en formato binario


class Capacitacion(db.Model):
    __tablename__ = 'CAPACITACION'
    id_capacitacion = db.Column(db.Integer, primary_key=True)
    id_empleado = db.Column(db.Integer, nullable=False)  # Relación con EMPLEADO
    nombre = db.Column(db.String(100), nullable=False)
    fecha_ini = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date)
    descripcion = db.Column(db.String(255))


class Contrato(db.Model):
    __tablename__ = 'CONTRATO'
    id_contrato = db.Column(db.Integer, primary_key=True)
    id_empleado = db.Column(db.Integer, nullable=False)  # Relación con EMPLEADO
    tipo_cont = db.Column(db.String(50), nullable=False)
    fec_ini = db.Column(db.Date, nullable=False)
    fec_fin = db.Column(db.Date)
    condiciones = db.Column(db.String(255))
    salario = db.Column(db.Integer)


class Departamento(db.Model):
    __tablename__ = 'DEPARTAMENTO'
    id_departamento = db.Column(db.Integer, primary_key=True)
    id_jefe = db.Column(db.Integer, nullable=False)  # Relación con el jefe (empleado)
    nom_departamento = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))

class Emplea(db.Model):
    __tablename__ = 'EMPLEA'
    id_acceso = db.Column(db.Integer, primary_key=True)
    id_rol = db.Column(db.Integer, primary_key=True)

class Empleado(db.Model):
    __tablename__ = 'EMPLEADO'
    id_empleado = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)  # Relación con USUARIO
    id_departamento_pertenece = db.Column(db.Integer, nullable=False)  # Relación con DEPARTAMENTO
    nombre = db.Column(db.String(50), nullable=False)
    ap_paterno = db.Column(db.String(50), nullable=False)
    ap_materno = db.Column(db.String(50))
    fec_nac = db.Column(db.Date)
    foto = db.Column(db.LargeBinary)  # Campo para almacenar fotos
    direccion = db.Column(db.String(255))
    cargo = db.Column(db.String(50))
    est_emp = db.Column(db.String(20))

class EvaluacionDesempeno(db.Model):
    __tablename__ = 'EVALUACION_DESEMPEÑO'
    id_evaluacion = db.Column(db.Integer, primary_key=True)
    id_candidato = db.Column(db.Integer, nullable=False)  # Relación con CANDIDATO
    id_empleado_realiza = db.Column(db.Integer, nullable=False)  # Relación con EMPLEADO
    id_empleado_genera = db.Column(db.Integer, nullable=False)  # Relación con EMPLEADO
    fecha_evaluacion = db.Column(db.Date, nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.String(255))

class Gestiona(db.Model):
    __tablename__ = 'GESTIONA'
    id_rol = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, primary_key=True)

class Historial(db.Model):
    __tablename__ = 'HISTORIAL'
    id_historial = db.Column(db.Integer, primary_key=True)
    id_empleado = db.Column(db.Integer, nullable=False)  # Relación con EMPLEADO
    fecha_cambio = db.Column(db.Date, nullable=False)
    tipo_cambio = db.Column(db.String(50), nullable=False)
    det_cambio = db.Column(db.String(255), nullable=False)
    mot_cambio = db.Column(db.String(255))

class Informe(db.Model):
    __tablename__ = 'INFORME'
    id_informe = db.Column(db.Integer, primary_key=True)
    id_empleado = db.Column(db.Integer, nullable=False)  # Relación con EMPLEADO
    fecha_informe = db.Column(db.Date, nullable=False)
    estado_informe = db.Column(db.String(50), nullable=False)
    tipo_informe = db.Column(db.String(50), nullable=False)
    criterio_busqueda = db.Column(db.String(100))

class Notifica(db.Model):
    __tablename__ = 'NOTIFICA'
    id_usuario_envia = db.Column(db.Integer, primary_key=True)
    id_usuario_recibe = db.Column(db.Integer, primary_key=True)
    fecha_notificacion = db.Column(db.Date, nullable=False)

class Participa(db.Model):
    __tablename__ = 'PARTICIPA'
    id_empleado = db.Column(db.Integer, primary_key=True)
    id_capacitacion = db.Column(db.Integer, primary_key=True)

class Permiso(db.Model):
    __tablename__ = 'PERMISO'
    id_permiso = db.Column(db.Integer, primary_key=True)
    id_empleado_aprobador = db.Column(db.Integer, nullable=False)
    id_empleado_solicitante = db.Column(db.Integer, nullable=False)
    tipo_permiso = db.Column(db.String(50), nullable=False)
    fecha_solicitud = db.Column(db.Date, nullable=False)
    fecha_aprobacion = db.Column(db.Date)
    estado = db.Column(db.String(20), nullable=False)

class Posee(db.Model):
    __tablename__ = 'POSEE'
    id_rol = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, primary_key=True)

class Postula(db.Model):
    __tablename__ = 'POSTULA'
    id_vacante = db.Column(db.Integer, primary_key=True)
    id_candidato = db.Column(db.Integer, primary_key=True)

class RegistroPago(db.Model):
    __tablename__ = 'REGISTRO_PAGO'
    id_pago = db.Column(db.Integer, primary_key=True)
    id_empleado = db.Column(db.Integer, nullable=False)
    id_caja = db.Column(db.Integer, nullable=False)
    id_afp = db.Column(db.Integer, nullable=False)
    fecha_gen = db.Column(db.Date, nullable=False)
    sueldo_base = db.Column(db.Integer, nullable=False)
    deducciones = db.Column(db.Integer, nullable=False)
    bonificaciones = db.Column(db.Integer, nullable=False)

class Rol(db.Model):
    __tablename__ = 'ROL'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(50), nullable=False)
    descripcion_rol = db.Column(db.String(255))

class Vacante(db.Model):
    __tablename__ = 'VACANTE'
    id_vacante = db.Column(db.Integer, primary_key=True)
    id_departamento = db.Column(db.Integer, nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    fec_publi = db.Column(db.Date)
