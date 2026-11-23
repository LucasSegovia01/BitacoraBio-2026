"""Capa de presentación: Carga de experimentos: rutas de registro (Flask). Reciben el pedido, llaman a un servicio y arman la respuesta.

No contienen reglas de negocio: solo pasan los datos del formulario al Ejecutor de registro y muestran
lo que responde (aviso de registro, coincidencias o errores traducidos por Gestión de excepciones).
"""
from __future__ import annotations

from datetime import date

from flask import Flask, Response, abort, render_template, request

from ..dominio.registro_tecnicas import RegistroDeTecnicas
from ..dominio.solicitud import DatosRegistro
from ..servicios.ejecutor_registro import EjecutorDeRegistro
from ..servicios.servicio_consulta import ServicioConsulta
from ..transversal.gestion_excepciones import ErrorPrevisto, respuesta_para

CANTIDAD_EXTRAS = 3


def _leer_datos(form, archivos) -> DatosRegistro:
    """Transcribe lo que llegó del formulario a DatosRegistro, sin validar nada."""
    tipo = form.get("tipo", "")
    valores, partes = {}, {}
    for clave, valor in form.items():
        if clave.startswith("v_"):
            nombre, _, indice = clave[2:].partition("__")
            if indice:  # valor compuesto en varias casillas (v_centro_caja__1, __2, __3): se une con coma
                partes.setdefault(nombre, []).append((indice, valor.strip()))
            else:
                valores[nombre] = valor
    for nombre, casillas in partes.items():
        textos = [t for _, t in sorted(casillas)]
        valores[nombre] = ", ".join(textos) if any(textos) else ""
    extras = []
    for i in range(1, CANTIDAD_EXTRAS + 1):
        nombre, valor = form.get(f"extra_nombre_{i}", "").strip(), form.get(f"extra_valor_{i}", "").strip()
        if nombre or valor:
            extras.append((nombre, valor, form.get(f"extra_unidad_{i}", "").strip() or None))
    try:
        fecha = date.fromisoformat(form.get("fecha_realizacion", ""))
    except ValueError:
        fecha = None
    pdb = None
    if archivos.get("pdb") and archivos["pdb"].filename:
        pdb = archivos["pdb"].read()
    return DatosRegistro(
        proyecto_id=form.get("proyecto_id", ""),
        tipo=tipo,
        fecha_realizacion=fecha,
        valores=valores,
        extras=extras,
        hardware=form.get("hardware", ""),
        tiempo_procesamiento=form.get("tiempo_procesamiento", ""),
        objetivo=form.get("objetivo", ""),
        hipotesis=form.get("hipotesis", ""),
        notas=form.get("notas", ""),
        similar_a=form.getlist("similar_a"),
        pdb=pdb,
    )


def crear_app(
    ejecutor: EjecutorDeRegistro,
    tecnicas: RegistroDeTecnicas,
    consulta: ServicioConsulta,
    autor: str,
) -> Flask:
    app = Flask(__name__)

    @app.context_processor
    def datos_de_pagina():
        return {"usuario": autor}

    def mostrar_formulario(tipo: str, form=None, mensajes=None, registrado=None):
        tecnica = tecnicas.tecnica(tipo)
        return render_template(
            "formulario.html",
            tecnicas=tecnicas.disponibles(),
            tecnica=tecnica,
            proyectos=consulta.proyectos(),
            experimentos=consulta.experimentos(),
            form=form or {},
            mensajes=mensajes or [],
            registrado=registrado,
            extras=range(1, CANTIDAD_EXTRAS + 1),
        )

    def con_manejo_de_errores(accion, tipo="docking"):
        try:
            return accion()
        except ErrorPrevisto as e:
            return mostrar_formulario(tipo, request.form, respuesta_para(e)["mensajes"]), 400

    @app.get("/")
    @app.get("/registro")
    def formulario():
        return mostrar_formulario(request.args.get("tipo") or tecnicas.disponibles()[0].tipo)

    @app.post("/registro")
    def registrar_experimento():
        datos = _leer_datos(request.form, request.files)

        def accion():
            resultado = ejecutor.registrar(datos, autor)
            if resultado.registrado:  # sin coincidencias: sigue en el formulario, con el aviso debajo
                return mostrar_formulario(datos.tipo, registrado=resultado.experimento)
            return render_template("coincidencias.html", coincidencias=resultado.coincidencias,
                                   pendiente_id=resultado.pendiente_id)

        return con_manejo_de_errores(accion, datos.tipo or "docking")

    @app.post("/registro/confirmar")
    def continuar_pese_a_coincidencia():
        def accion():
            resultado = ejecutor.confirmar(request.form.get("pendiente_id", ""))
            return render_template("resultado.html", experimento=resultado.experimento)

        return con_manejo_de_errores(accion)

    @app.post("/registro/cancelar")
    def cancelar_registro():
        ejecutor.cancelar(request.form.get("pendiente_id", ""))
        return render_template("cancelado.html")

    # Pantallas de consulta: solo leen lo guardado a través de ServicioConsulta (no son parte de HU-01.A1).
    def conteos(experimentos):
        c = {"total": len(experimentos), "finalizado": 0, "en_curso": 0, "invalido": 0}
        for e in experimentos:
            c[e.estado_validez] += 1
        return c

    def nombres():
        return dict(consulta.proyectos())

    @app.get("/experimentos")
    def mis_experimentos():
        estado = request.args.get("estado", "")
        propios = consulta.de_autor(autor)
        return render_template("mis_experimentos.html", experimentos=[e for e in propios if not estado or e.estado_validez == estado],
                               conteos=conteos(propios), estado=estado, nombres=nombres())

    @app.get("/experimentos/<experimento_id>")
    def detalle_experimento(experimento_id):
        e = consulta.experimento(experimento_id)
        if e is None:
            abort(404)
        etiquetas = {d.nombre: d.etiqueta for d in tecnicas.tecnica(e.tipo).definiciones()}
        return render_template("detalle_experimento.html", e=e, nombre_proyecto=consulta.nombre_de_proyecto(e.proyecto_id),
                               etiquetas=etiquetas)

    @app.get("/experimentos/<experimento_id>/pdb")
    def pdb_del_experimento(experimento_id):
        e = consulta.experimento(experimento_id)
        contenido = consulta.contenido_pdb(e) if e else None
        if contenido is None:
            abort(404)
        return Response(contenido, mimetype="text/plain")

    @app.get("/proyectos")
    def listado_de_proyectos():
        return render_template("proyectos.html", proyectos=consulta.resumen_de_proyectos())

    @app.get("/proyectos/<proyecto_id>")
    def detalle_de_proyecto(proyecto_id):
        proyecto = consulta.proyecto(proyecto_id)
        if proyecto is None:
            abort(404)
        experimentos = consulta.experimentos_de(proyecto_id)
        return render_template("proyecto_detalle.html", proyecto=proyecto, experimentos=experimentos, conteos=conteos(experimentos))

    @app.get("/buscar")
    def buscar():
        filtros = {k: request.args.get(k, "").strip() for k in ("q", "autor", "proyecto", "estado")}
        resultados = consulta.buscar(filtros["q"], filtros["proyecto"], filtros["autor"], filtros["estado"])
        return render_template("busqueda.html", filtros=filtros, resultados=resultados, autores=consulta.autores(),
                               proyectos=consulta.proyectos(), nombres=nombres())

    @app.get("/ayuda")
    def ayuda():
        return render_template("ayuda.html")

    return app
