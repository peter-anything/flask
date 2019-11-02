from flask import request
from flask_graphql import GraphQLView
import jenkins
import xml.etree.cElementTree as ET
from xml.sax.saxutils import escape
import os
import ujson as json

from apps.jenkins.views import blue_print
from apps.common import JSONResponse, Status
from apps.jenkins.models import Job
from apps.jenkins.models import JobSchema


def handle_job_create_or_update(req):
    params = req.get_json()
    name = params.get('name')
    pipeline_script = params.get('pipeline_script')
    print(params.get('build_parms').strip())
    build_parms = json.loads(params.get('build_parms').strip())
    print(build_parms)
    if not (name and pipeline_script):

        return JSONResponse.error('name and pipeline_script must be provided')
    else:
        job = Job.query.filter_by(name=name).first()
        if job:
            job.pipeline_script = pipeline_script
            job.status = Status.VALID
            job.build_parms = json.dumps(build_parms)
            job.save()
        else:
            job = Job(name=name,
                      pipeline_script=pipeline_script,
                      build_parms=json.dumps(build_parms)
                      )
            job.save()

        return JSONResponse.success()


@blue_print.route('/job/create', methods=['POST'])
def job_create():
    print('create')
    return handle_job_create_or_update(request)


@blue_print.route('/job/update', methods=['PUT'])
def job_update():
    return handle_job_create_or_update(request)


@blue_print.route('/job/delete', methods=['POST'])
def job_delete():
    params = request.get_json()
    name = params.get('name')
    Job.query.filter_by(name=name).update({Job.status: Status.DELETED})

    return JSONResponse.success()


@blue_print.route('/job/list', methods=['GET'])
def job_list():
    ret_jobs = []
    jobs = Job.query.filter(Job.status == Status.VALID).order_by(Job.updated_time.desc()).all()
    for job in jobs:
        ret_jobs.append({
            'id': job.id,
            'name': job.name,
            'pipeline_script': job.pipeline_script,
            'build_parms': job.build_parms,
            'status': job.status.value
        })

    return JSONResponse.success({
        'records': ret_jobs,
        'count': len(ret_jobs)
    })


@blue_print.route('/job/sync', methods=['POST'])
def job_sync():
    params = request.get_json()
    name = params.get('name')
    if not name:
        return JSONResponse.error('name must be provided')

    job = Job.query.filter(Job.name == name, Job.status == Status.VALID).first()
    if job:
        jenkins_url = 'http://peter:113ee50dcf68fec1ce1a1a68823bc1d1ad@jenkins.gsir.com.cn'
        server = jenkins.Jenkins(jenkins_url)
        config_dir = os.path.dirname(os.path.dirname(__file__))
        tree = ET.ElementTree(file='%s/config/config_template.xml' % config_dir)
        script = job.pipeline_script
        for elem in tree.iterfind('definition/script'):
            elem.text = escape(script)
        xml_str = ET.tostring(tree.getroot(), encoding='utf-8')
        if job.synced:
            server.reconfig_job(job.name, xml_str.decode('utf-8'))
        else:
            job.synced = True
            server.create_job(job.name, xml_str.decode('utf-8'))
            job.save()

        server.build_job(job.name)

        return JSONResponse.success()


@blue_print.route('/job/send-task', methods=['POST'])
def job_send_task():
    params = request.get_json()
    name = params.get('name')
    if not name:
        return JSONResponse.error('name must be provided')

    job = Job.query.filter(Job.name == name, Job.status == Status.VALID).first()
    if job:
        jenkins_url = 'http://peter:113ee50dcf68fec1ce1a1a68823bc1d1ad@jenkins.gsir.com.cn'
        server = jenkins.Jenkins(jenkins_url)
        print(json.loads(job.build_parms))
        print(name)
        server.build_job(name, parameters=json.loads(job.build_parms))

        return JSONResponse.success()

    else:

        return JSONResponse.error('Job not exist!')


blue_print.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=JobSchema,
        graphiql=True  # for having the GraphiQL interface
    )
)
