# coding=utf8

from app import db
from flask import  url_for


class MailUser(db.Model):
    '''
        mailuser
    '''
    __tablename__ = "MailUser"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), index=True, unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class Users(db.Model):
    """
    普通用户model
    """
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False, index=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    regDate = db.Column(db.String(50), nullable=False)
    isActive = db.Column(db.Boolean, nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False)

    def __init__(self, email, username, password, regDate, isActive=False, isAdmin=False):
        self.email = email
        self.username = username
        self.password = password
        self.regDate = regDate
        self.isActive = isActive
        self.isAdmin = isAdmin

    """
    flask-login必须实现的接口
    """

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        if self.isAdmin is False:
            return False  # 不能登录后台
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


class InviteCodeList(db.Model):
    """
    邀请码表
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    inviteCode = db.Column(db.String(50), index=True, nullable=False, unique=True)
    codestatus = db.Column(db.Boolean, nullable=False)

    def __init__(self, inviteCode, codestatus=True):
        self.inviteCode = inviteCode
        self.codestatus = codestatus


class User(db.Model):
    """
    报告专用用户表普通用户表
    """
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(150), unique=True, nullable=False, index=True)
    passwd = db.Column(db.String(150), nullable=False)
    regDate = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey('Role.id'))

    def __init__(self, username, password, regDate, email, role_id):
        self.uname = username
        self.passwd = password
        self.regDate = regDate
        self.email = email
        self.role_id

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


class Role(db.Model):
    """
    角色
    """
    __tablename__ = 'Role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rolename = db.Column(db.String(150), unique=True, nullable=False, index=True)

    def __init__(self, rolename):
        self.rolename = rolename


class Project(db.Model):
    """
        项目
    """
    __tablename__ = "Project"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projectname = db.Column(db.String(50), nullable=False)
    projectnum = db.Column(db.Integer, nullable=False)
    # 模块,具体用途为测试报告所使用
    # module = db.Column(db.String(50))

    def __init__(self, projectname, projectnum, member='null', report_id='null'):
        self.projectname = projectname
        self.projectnum = projectnum


class Report(db.Model):
    """
        report
    """
    __tablename__ = "Report"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
 #   project_id = db.Column(db.Integer, db.ForeignKey('Project.id'))
 #   project_module = db.Column(db.String(50))
 #   user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    # 渗透测试IP
    ip = db.Column(db.String(50))
    # 渗透测试开始时间
    start_time = db.Column(db.String(50))
    # 渗透测试结束时间
    end_time = db.Column(db.String(50))
    # 报告作者
    author = db.Column(db.String(50), nullable=False)

    def __init__(self, name, type, date, ip, start_time, end_time, author):
        self.name = name
        self.type = type
        self.date = date
#        self.project_id = project_id
#        self.project_module = project_module
#        self.user_id = user_id
        self.ip = ip
        self.start_time = start_time
        self.end_time = end_time
        self.author = author


    def to_json(self):
        json_report = {
            'url': url_for('homes.get_report',id=self.id, _external=True),
            'date': self.date,
            'type': self.type,
            'name': self.name,
            'ip': self.ip,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'author': self.author
        }
        return json_report
    @staticmethod
    def from_json(json_report):
        name = json_report['name']
        type = json_report['type']
        date = json_report['date']
        ip = json_report['ip']
        start_time = json_report['start_time']
        end_time = json_report['end_time']
        author = json_report['author']
        if name is None or name =='':
            pass
        return Report(name, type, date, ip, start_time, end_time, author)

class Attatchments(db.Model):
    """
        附件
    """
    __tablename__ = "Attatchments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('Project.id'))

    def __init__(self, filename, description, report_id):
        self.filename = filename
        self.description = description
        self.report_id = report_id


class TemplateVulnerability(db.Model):
    """
        漏洞模板
    """
    __tablename__ = "TemplateVulnerability"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), unique=True,nullable=True)
    damage = db.Column(db.String(100))
    type = db.Column(db.String(50))
    # 风险分析
    overview = db.Column(db.Text)
    # #影响主机
    # affected_hosts = db.Column(db.String(50))
    # 验证过程
    poc = db.Column(db.Text)
    # 风险等级
    risk = db.Column(db.String(50), nullable=True)
    # 修复建议
    remediation = db.Column(db.Text)

    def __init__(self, title, type, risk, overview, poc, damage, remediation):
        self.title = title
        self.damage = damage
        self.type = type
        self.overview = overview
        self.poc = poc
        self.risk = risk
        self.remediation = remediation

    def to_json(self):
        json_temVuln = {
            'url':url_for('homes.get_vuln',id=self.id, _external=True),
            'title':self.title,
            'type':self.type,
            'damage':self.damage,
            'overview':self.overview,
            'poc':self.poc,
            'risk':self.risk,
            'remediation':self.remediation
        }
        return json_temVuln

    @staticmethod
    def from_json(json_temVuln):
        title = json_temVuln['title']
        type = json_temVuln['type']
        damage = json_temVuln['damage']
        overview = json_temVuln['overview']
        poc = json_temVuln['poc']
        risk = json_temVuln['risk']
        remediation = json_temVuln['remediation']
        if title is None or title =='':
            pass
        return TemplateVulnerability(title, type, risk, overview, poc, damage, remediation)


class Vulnerability(db.Model):
    """
        漏洞
    """
    __tablename__ = "Vulnerability"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=True)
    damage = db.Column(db.String(100))
    report_id = db.Column(db.Integer, db.ForeignKey('Report.id'))
    type = db.Column(db.String(50))
    # 风险分析
    overview = db.Column(db.Text)
    # 影响主机
    ip = db.Column(db.Text)
    # 验证过程
    poc = db.Column(db.Text)
    # 风险等级
    risk = db.Column(db.String(50), nullable=True)
    # 修复建议
    remediation = db.Column(db.Text)

    def __init__(self, title, damage, report_id, type, overview, ip, poc, risk, remediation):
        self.title = title
        self.damage = damage
        self.report_id = report_id
        self.type = type
        self.overview = overview
        self.ip = ip
        self.poc = poc
        self.risk = risk
        self.remediation = remediation

    def to_json(self):
        json_Vuln = {
            'url': url_for('homes.get_report_vuln', id=self.report_id, vuln_id=self.id, _external=True),
            'title': self.title,
            'damage': self.damage,
            'report_id': self.report_id,
            'type': self.type,
            'overview': self.overview,
            'ip': self.ip,
            'poc': self.poc,
            'risk': self.risk,
            'remediation': self.remediation
        }
        return json_Vuln

    @staticmethod
    def from_json(json_Vuln):
        title = json_Vuln['title']
        damage = json_Vuln['damage']
        report_id = json_Vuln['report_id']
        type = json_Vuln['type']
        overview = json_Vuln['overview']
        ip = json_Vuln['ip']
        poc = json_Vuln['poc']
        risk = json_Vuln['risk']
        remediation = json_Vuln['remediation']
        if title is None or title =='':
            pass
        return Vulnerability(title, damage, report_id, type, overview, ip, poc, risk, remediation)