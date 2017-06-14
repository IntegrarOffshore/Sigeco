# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

# VIEWS

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))
    
@auth.requires_login()
def level():
    contador = db(db.funcionario.status != "Concluido").count()
    if contador == 0:
        response.flash = 'Nenhum atendimento pendente'
    elif contador == 1:
        response.flash = 'Existe %s atendimento pendente' % contador
    else:
        response.flash = 'Existem %s atendimentos pendentes' % contador
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

# CREATE

# @auth.requires_login()
# @auth.requires_membership('funcionario')

@auth.requires_login()
def funcionario():
    form = SQLFORM(Funcionario)
    if form.process().accepted:
        session.flash = 'Atendimento para %s cadastrado' % form.vars.nome
        agora = request.now
        createdby = auth.user.id
        createdbyn = auth.user.first_name
        db(db.funcionario.created_by == createdby).update(atendente=createdbyn)
        db(db.funcionario.created_on == agora).update(dia=agora)
        redirect(URL('funcionario'))
    elif form.errors:
        response.flash = 'Erros encontrados no formulário'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário'
    return dict(form=form)

# READ

@auth.requires_login()
def ver_funcionario():
    try:
        grupo = auth.user_groups
        if grupo[2] == 'gerente':
            grid = SQLFORM.grid(Funcionario, formstyle = 'table3cols', fields=[db.funcionario.nome, db.funcionario.plataforma,db.funcionario.assunto, db.funcionario.status, db.funcionario.atendente, db.funcionario.dia], create=False, exportclasses=dict(tsv_with_hidden_cols=False, csv=False, xml=False, json=False))
            return dict(grid=grid)
        else:
            db.funcionario.dia.writable = False
            db.funcionario.atendente.writable = False
            grid = SQLFORM.grid(Funcionario, fields=[db.funcionario.nome, db.funcionario.plataforma,db.funcionario.assunto, db.funcionario.status, db.funcionario.atendente, db.funcionario.dia], create=False, deletable=False, exportclasses=dict(tsv_with_hidden_cols=False, csv=False, xml=False, json=False))
            return dict(grid=grid)
    except:
        db.funcionario.dia.writable = False
        db.funcionario.atendente.writable = False
        grid = SQLFORM.grid(Funcionario, fields=[db.funcionario.nome, db.funcionario.plataforma,db.funcionario.assunto, db.funcionario.status, db.funcionario.atendente, db.funcionario.dia], create=False, deletable=False, exportclasses=dict(tsv_with_hidden_cols=False, csv=False, xml=False, json=False))
        return dict(grid=grid)

@auth.requires_login()
def ver_usuarios():
    grid = SQLFORM.grid(db.auth_user, create=False, deletable=False, exportclasses=dict(tsv_with_hidden_cols=False, csv=False, xml=False, json=False))
    return dict(grid=grid)

def ver_funcionario_pendente():
    try:
        grupo = auth.user_groups
        if grupo[2] == 'gerente':
            query = ((db.funcionario.status == 'Aberto'))
            grid = SQLFORM.grid(query=query, formstyle = 'table3cols', fields=[db.funcionario.nome, db.funcionario.plataforma,db.funcionario.assunto, db.funcionario.status, db.funcionario.atendente, db.funcionario.dia], create=False, exportclasses=dict(tsv_with_hidden_cols=False, csv=False, xml=False, json=False))
            return dict(grid=grid)
    except:
        db.funcionario.dia.writable = False
        db.funcionario.atendente.writable = False
        query = ((db.funcionario.status == 'Aberto'))
        grid = SQLFORM.grid(query=query, fields=[db.funcionario.nome, db.funcionario.plataforma,db.funcionario.assunto, db.funcionario.status, db.funcionario.atendente, db.funcionario.dia], create=False, deletable=False, exportclasses=dict(tsv_with_hidden_cols=False, csv=False, xml=False, json=False))
        return dict(grid=grid)

@auth.requires_login()
def ver_usuarios():
    grid = SQLFORM.grid(db.auth_user, create=False, deletable=False, exportclasses=dict(tsv_with_hidden_cols=False, csv=False, xml=False, json=False))
    return dict(grid=grid)

# EDIT

#@auth.requires_membership('funcionario')
@auth.requires_login()
def editar_aluno():
    form = SQLFORM(Aluno, request.args(0, cast=int), showid = False)
    if form.process().accepted:
        session.flash = 'Aluno atualizado: %s' % form.vars.nome
        redirect(URL('ver_aluno'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        response.flash = 'Preencha o formulário!'
    return dict(form=form)

# DELETE
@auth.requires_login()
#@auth.requires_membership('funcionario')
def deletar_aluno():
    db(Aluno.id==request.args(0, cast=int)).delete()
    session.flash = 'Aluno excluido'
    redirect(URL('ver_aluno'))
