# coding=utf8

from flask import Blueprint, request, render_template, session, \
    jsonify, url_for, redirect, send_file,send_from_directory
from app import app, db
from util.util import getPasswordMd5, getTimeNow, isEmailString, ValidCode
from app.models import Report, Users, InviteCodeList, TemplateVulnerability,Vulnerability
from flask.ext.login import login_required, login_user, logout_user
from docx import Document
from docx.shared import Inches
from cStringIO import StringIO
import StringIO

homes = Blueprint("homes", __name__, static_folder='static', template_folder='templates')


@homes.route("/index", methods=["GET", "POST"])
@login_required
def index():
    return render_template("home/index/pages/index.html")


@homes.route('/', methods=["GET", "POST"])
@homes.route('/login', methods=["GET", "POST"])
def login():
    """
    用户登录视图
    :return:
    """
    if request.method == "GET":
        return render_template("home/login.html")
    elif request.method == "POST":
        username = request.json["username"]
        password = request.json["password"]
        yzCode = request.json["yzCode"]
        try:
            session_yzCode = session["yzCode"]
            if getPasswordMd5(yzCode.lower(), "O(@(#@EJW@!JIEW") != session_yzCode:
                session.pop("yzCode", None)
                return jsonify({"status": "yzcode", "msg": "验证码错误"})
        except:
            return jsonify({"status": "yzcode", "msg": "验证码错误"})
        if isEmailString(username):  # email形式登录
            users = Users.query.filter_by(email=username).first()
        else:
            users = Users.query.filter_by(username=username).first()

        if users != None:
            password_md5 = getPasswordMd5(password, users.regDate)
            if password_md5 == users.password:  # 登录成功
                login_user(users)
                session.permanent = True
                return jsonify({"status": "success", "url": url_for("homes.index")})

        return jsonify({"status": "failed", "msg": "用户名或密码错误"})


@homes.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("homes.login"))


@homes.route('/register', methods=["GET", "POST"])
def register():
    """
    用户注册视图
    :return:
    """
    if request.method == "GET":
        return render_template("home/register.html")
    elif request.method == "POST":
        inviteCode = request.json['invitecode']
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        if not isEmailString(email):
            return jsonify({"stauts": "failed", "msg": "请输入正确的邮箱"})
        regDate = getTimeNow()
        try:
            invicode = InviteCodeList.query.filter_by(inviteCode=inviteCode).first()
            if invicode.codestatus == True:
                try:
                    users = Users(email, username, getPasswordMd5(password, str(regDate)), regDate)
                    db.session.add(users)
                    # db.session.commit()
                    # 邀请码失效
                    invicode.codestatus = False
                    db.session.commit()
                    return jsonify({"status": "success", "url": url_for("homes.login")})
                except:
                    return jsonify({"status": "failed", "msg": "填写的信息有误"})
            else:
                return jsonify({"status": "failed", "msg": "邀请码已被使用"})
        except:
            return jsonify({"status": "failed", "msg": "邀请码有误"})


@homes.route('/forgetpass', methods=["GET", "POST"])
def forgetpass():
    """
    用户忘记密码视图
    :return:
    """
    if request.method == "GET":
        return render_template("home/forgetpass.html")


@homes.route('/randomcode/<rand>', methods=["GET"])
def randomcode(rand):
    """
    验证码视图
    :param rand:
    :return:
    """
    if request.method == "GET":
        validcode = ValidCode()
        code_img, strs = validcode.drawCode()  # 验证码
        session['yzCode'] = getPasswordMd5(strs.lower(), "O(@(#@EJW@!JIEW")
        buf = StringIO.StringIO()
        code_img.save(buf, 'JPEG', quality=70)
        buf_str = buf.getvalue()
        response = app.make_response(buf_str)
        response.headers['Content-Type'] = 'image/jpeg'
        return response


@homes.route('/vuln/', methods=["GET", "POST"])
@login_required
def vuln():
    return render_template("home/index/pages/replatform/vuln.html")

@homes.route('/vuln/list', methods=["GET", "POST"])
# @homes.route('/vuln/page/<int:page>', methods=["GET", "POST"])
@login_required
def list_vulns():
    '''
    获取漏洞,添加漏洞
    :param action:
    :return:
    '''
    #分页后续再做,暂时不研究了,浪费时间
    # if request.method == "GET":
    #     page = request.args.get('page', 1, type=int)
    #     page_sum = 10
    #     pagination = TemplateVulnerability.query.paginate(page, page_sum, False)
    #     vulns = pagination.items
    #     prev = None
    #     if pagination.has_prev:
    #         prev = url_for('homes.list_vulns', page=page - 1, _external=False)
    #         # prev = page - 1
    #     next = None
    #     if pagination.has_next:
    #         next = url_for('homes.list_vulns', page=page + 1, _external=False)
    #         # next = page + 1
    #     return jsonify({'vulns': [vuln.to_json() for vuln in vulns],
    #                     'prev': prev,
    #                     'next': next,
    #                     'count': pagination.total
    #                     })
    vulns = TemplateVulnerability.query.all()
    count = TemplateVulnerability.query.count()
    return jsonify({'vulns': [vuln.to_json() for vuln in vulns],
                    'count': count
                    })

@homes.route('/vuln/<int:id>', methods=["GET", "PUT", "DELETE", "POST"])
@login_required
def get_vuln(id):
    '''
    获取,修改,删除单个漏洞,
    :param action:
    :return:
    '''
    if request.method == "GET":
        vuln = TemplateVulnerability.query.get_or_404(id)
        return render_template("home/index/pages/replatform/addReportVuln.html", vuln=vuln)

    elif request.method == "PUT":
        vuln = TemplateVulnerability.query.get_or_404(id)
        vuln.type = request.json.get('type', vuln.type)
        vuln.damage = request.json.get('damage', vuln.damage)
        vuln.overview = request.json.get('overview', vuln.overview)
        vuln.poc = request.json.get('poc', vuln.poc)
        vuln.risk = request.json.get('risk', vuln.risk)
        vuln.remediation = request.json.get('remediation', vuln.remediation)
        db.session.add(vuln)
        db.session.commit()
        return jsonify({"status": "success", "msg": "修改成功"})

    elif request.method == "DELETE":
        vuln = TemplateVulnerability.query.get_or_404(id)
        db.session.delete(vuln)
        db.session.commit()
        return jsonify({"status": "success", "msg": "删除成功"})


@homes.route('/addvuln/', methods=["GET", "POST"])
@login_required
def add_vuln():
    """
    添加漏洞
    :return:
    """
    if request.method == "GET":
        return render_template("home/index/pages/replatform/addvuln.html")
    elif request.method == "POST":
        vuln = TemplateVulnerability.from_json(request.json)
        db.session.add(vuln)
        db.session.commit()
        return jsonify({'msg': "success"})

@homes.route('/report/', methods=["GET", "POST"])
@login_required
def report():
    return render_template("home/index/pages/replatform/report.html")

@homes.route('/report/list/', methods=["GET", "POST"])
# @homes.route('/report/page/<int:page>', methods=["GET", "POST"])
@login_required
def list_report():
    '''
    获取漏洞,添加漏洞
    :param action:
    :return:
    '''
    if request.method == "GET":
        reports = Report.query.all()
        count = Report.query.count()
        return jsonify({'reports': [report.to_json() for report in reports],
                        'count': count
                        })


@homes.route('/report/add', methods=["GET", "POST"])
@login_required
def add_report():
    """
    添加漏洞
    :return:
    """
    if request.method == "GET":
        return render_template("home/index/pages/replatform/addreport.html")
    elif request.method == "POST":
        report = Report.from_json(request.json)
        db.session.add(report)
        db.session.commit()
        return jsonify({'msg': "success"})


@homes.route('/report/<int:id>', methods=["GET", "PUT", "DELETE", "POST"])
@login_required
def get_report(id):
    '''
    获取,修改,删除报告,
    :param action:
    :return:
    '''
    if request.method == "GET":
        report = Report.query.get_or_404(id)
        return render_template("home/index/pages/replatform/addreport.html", report=report)

    elif request.method == "PUT":
        report = Report.query.get_or_404(id)
        report.name = request.json.get('name', report.name)
        report.type = request.json.get('type', report.type)
        report.ip = request.json.get('ip', report.ip)
        report.date = request.json.get('date', report.date)
        report.author = request.json.get('author', report.author)
        report.start_time = request.json.get('start_time', report.start_time)
        report.end_time = request.json.get('end_time', report.end_time)
        db.session.add(report)
        db.session.commit()
        return jsonify({"status": "success", "msg": "修改成功"})

    elif request.method == "DELETE":
        report = Report.query.get_or_404(id)
        db.session.delete(report)
        db.session.commit()
        return jsonify({"status": "success", "msg": "删除成功"})


@homes.route('/report/<int:id>/vuln', methods=["GET", "POST"])
@login_required
def get_report_vuln_list(id):
    '''
    获取漏洞库,新增漏洞,
    :param action:
    :return:
    '''
    # vuln = TemplateVulnerability.query.get_or_404(id)
    if request.method == "GET":
        report = Report.query.get_or_404(id)
        vulns = TemplateVulnerability.query.all()
        count = TemplateVulnerability.query.count()
        return render_template("home/index/pages/replatform/report_add_vuln.html", vulns=vulns, count=count, report=report)
    if request.method == "POST":
        vulns=request.json.get('vulns')
        for vuln_id in vulns:
            if vuln_id == ',':
                continue
            else:
                Templatevuln = TemplateVulnerability.query.get_or_404(vuln_id)
                title = Templatevuln.title
                damage = Templatevuln.damage
                report_id = id
                type = Templatevuln.type
                overview = Templatevuln.overview
                ip = ''
                poc = Templatevuln.poc
                risk = Templatevuln.risk
                remediation = Templatevuln.remediation
                vuln = Vulnerability(title, damage, report_id, type, overview, ip, poc, risk, remediation)
                db.session.add(vuln)
                db.session.commit()
        return jsonify({"status": "success", "msg": '添加成功'})

@homes.route('/report/<int:id>/vulns', methods=["GET", "POST"])
@login_required
def get_report_vulns(id):
    '''
    获取报告当前漏洞,编辑当前漏洞
    :param action:
    :return:
    '''
    if request.method == "GET":
        vulns = Vulnerability.query.filter_by(report_id=id).all()
        count = Vulnerability.query.filter_by(report_id=id).count()
        return jsonify({'vulns': [vuln.to_json() for vuln in vulns],
                        'count': count
                        })

@homes.route('/report/<int:id>/vuln/<int:vuln_id>', methods=["GET", "POST", "PUT", "DELETE"])
@login_required
def get_report_vuln(id,vuln_id):
    '''
    获取,修改,删除单个漏洞,
    :param action:
    :return:
    '''
    if request.method == "GET":
        vuln = Vulnerability.query.get_or_404(vuln_id)
        return render_template("home/index/pages/replatform/addReportVuln.html", vuln=vuln)

    elif request.method == "PUT":
        vuln = Vulnerability.query.get_or_404(vuln_id)
        vuln.title = request.json.get('title', vuln.title)
        vuln.damage = request.json.get('damage', vuln.damage)
        vuln.type = request.json.get('type', vuln.type)
        vuln.overview = request.json.get('overview', vuln.overview)
        vuln.ip = request.json.get('ip', vuln.ip)
        vuln.poc = request.json.get('poc', vuln.poc)
        vuln.risk = request.json.get('risk', vuln.risk)
        vuln.remediation = request.json.get('remediation', vuln.remediation)
        db.session.add(vuln)
        db.session.commit()
        return jsonify({"status": "success", "msg": "修改成功"})

    elif request.method == "DELETE":
        vuln = Vulnerability.query.get_or_404(vuln_id)
        db.session.delete(vuln)
        db.session.commit()
        return jsonify({"status": "success", "msg": "删除成功"})

@homes.route('/report/<int:id>/create_vuln/', methods=["GET", "POST", "PUT", "DELETE"])
@login_required
def new_report_vuln(id):
    if request.method == "GET":
        report = Report.query.get_or_404(id)
        return render_template("home/index/pages/replatform/addReportVuln.html", report=report)

    elif request.method == "POST":
        title = request.json.get('title')
        damage = request.json.get('damage')
        report_id = id
        type = request.json.get('type')
        overview = request.json.get('overview')
        ip = request.json.get('ip')
        poc = request.json.get('poc')
        risk = request.json.get('risk')
        remediation = request.json.get('remediation')
        vuln = Vulnerability(title, damage, report_id, type, overview, ip, poc, risk, remediation)
        db.session.add(vuln)
        db.session.commit()
        return jsonify({"status": "success", 'msg': "添加成功"})
@homes.route('/report/<int:id>/export/', methods=["GET", "POST"])
@login_required
def report_export(id):
    if request.method == "GET":
        report = Report.query.get_or_404(id)
        document = Document('绿盟科技中央业务部web渗透测试模板.docx')
        filename = report.name+'.docx'
        document.save(filename)
        return send_from_directory('/Users/helit/helit/develop/webtool', filename)
