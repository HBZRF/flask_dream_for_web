from flask import Flask,render_template,url_for,redirect,request,make_response,g,send_from_directory,flash
from functools import wraps
import time
from flask import session
from flask_cors import CORS, cross_origin
from DBoperate import *
import os
import datetime
import json,math
from werkzeug import secure_filename
from flask import jsonify
import uuid
from flask import Blueprint
UPLOAD_FOLDER = '/home/python/bussise/static/uploadfile/pictures'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
SERVER_NAME = '0861.info'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PERMANENT_SESSION_LIFETIME']=datetime.timedelta(days=7)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True, resources=r'/*')


bp = Blueprint('app', __name__,
                        template_folder='templates')


def timestamp_toString(sp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sp))

@app.before_request
def before_request():
    if request.cookies.get("username",None) and request.cookies.get('password',None):
        filters = {'usr_id': request.cookies.get("username"),'pwd': request.cookies.get('password')}
        res = mysql_get_info(user, filters)
        if res:
            current_user_type = res[0].usr_type
            g.user = request.cookies.get("username")
            g.usr_type = current_user_type
        else:
            g.usr_type = None
            g.user = None
    else:

        g.usr_type = None
        g.user = None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.usr_type is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/logout/',methods=['GET'])
def logout():
    resp = make_response(redirect(url_for('goodsoverview')))
    resp.set_cookie("username", '')
    resp.set_cookie("password", '', max_age=360000)
    return resp
@app.route('/login/',methods=['POST','GET'])
def login():
    try:
        print(next)
    except:
        pass
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        pwd = request.form.get('password')
        filters = {'usr_id':username,'pwd':pwd}
        res = mysql_get_info(user, filters)
        if res:
            g.usr_type =res[0].usr_type
            rss = request.args.get("next")
            if rss:
                resp = make_response(redirect(rss))
                resp.set_cookie("username", res[0].usr_id)
                resp.set_cookie("password", res[0].pwd, max_age=360000)
                return resp

            resp = make_response(redirect(url_for('goodsoverview')))
            resp.set_cookie("username", res[0].usr_id)
            resp.set_cookie("password", res[0].pwd, max_age=360000)
            return resp
        else:
            return '密码错误！'


def allowed_file(filename):
    """
    上传的文件类型
    :param filename: 传入的文件名
    :return: 返回True 或者 False
    """
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


@cross_origin()
@app.route('/addgoods/',methods=['POST','GET'])
@login_required
def addgoods():
    if g.usr_type !='admin':
        return '无权访问！！'
    if request.method == 'GET':
        if request.is_xhr:
            goodcode = request.args.get('goodcode')
            filter = {'goodcode': goodcode}
            content = mysql_get_info(table_Goodinfo, filter)
            if content:
                print(content[0])
                rexx = json.dumps(content[0].to_dict())
            else:
                return '未找到相关货物'
            return jsonify(rexx)

        filter = {'usr_type':g.usr_type}
        return render_template('addgoods.html', **filter)
    else:
        nbr = request.form.get('goodcode')
        filters = {}
        filters['goodcode'] = nbr
        res = mysql_get_info(table_Goodinfo, filters)
        print(res)
        if res:
            return '货物号信息重复，请更正！（Repetition of goodscode，pls modify the goodscode!）'
        else:

            rs = request.form.to_dict()
            for key,value in rs.items():
                if not value:
                    return '''<HTML>
        <body>
         <P><font color="red"><H1>%s为空，请正确填写！</H1></font></P>
        </body>
    </html>'''%key
            filters = {}
            filters['goodcode'] = request.form.get('goodcode')
            files = request.files.getlist('photo1')
            tmp_files_name = ''
            for file in files:
                if file and allowed_file(file.filename):
                    print('写图片了')
                    Pic1Name1 = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], Pic1Name1))
                    tmp_files_name = tmp_files_name + Pic1Name1 + ';'
            key_value_dict = request.form.to_dict()
            key_value_dict['Pic1Name1'] = tmp_files_name
            #默认新增的货物不显示到首页
            key_value_dict['ishaspic'] = 1
            return mysql_add_info(table_Goodinfo, key_value_dict)

@cross_origin()
@app.route('/addgoodsinfo/',methods=['POST','GET'])
@login_required
def addgoodsinfo():
    if g.usr_type !='admin':
        return '无权访问！！'
    if request.method == 'GET':
        filter = {'usr_type':g.usr_type}
        return render_template('addgoodsinfo.html', **filter)
    else:
        if request.is_xhr:
            nbr = request.form.get('SerialNumber')
            filters = {}
            filters['SerialNumber'] = nbr
            res = mysql_get_info(table_Goods, filters)
            print(res)
            if res:
                content = res[0].to_dict()
                content['SerialNumber'] = nbr
                if g.usr_type =='admin':
                    pass
                else:
                    try:
                        content.pop('OrderId')
                        content.pop('factory')
                        content.pop('shizai')
                    except:
                        pass
                rexx = json.dumps(content)
                return jsonify(rexx)
            else:
                return '货物信息不存在！（no futher info,pls check the goods SerialNumber! ）'
        rs = request.form.to_dict()
        for key,value in rs.items():
            if not value:
                return '''<HTML>
    <body>
     <P><font color="red"><H1>%s为空，请正确填写！</H1></font></P>
    </body>
</html>'''%key
        filters = {}
        filters['SerialNumber'] = request.form.get('SerialNumber')

        key_value_dict = request.form.to_dict()

        key_value_dict['ishaspic'] = 1
        get_res = mysql_get_info(table_Goods,filters)
        if get_res:
            if g.usr_type == '999admin':
                print(key_value_dict)
                return mysql_update_info(get_res, key_value_dict)
            else:
                return '串号信息重复，请更正串号信息！（Repetition of serial numbers，pls modify the serial number!）'
        else:
            return mysql_add_info(table_Goods, key_value_dict)

@app.route('/<int:nbr>/',methods=['GET'])
def goodsinfo(nbr):
    if request.method == 'GET':
        print(g.usr_type)
        filters = {}
        filters['goodcode'] = nbr
        res = mysql_get_info(table_Goodinfo, filters)
        if res:
            content = res[0].to_dict()
            print('dddkkk')
            print(content)
            return render_template('goodsinfo.html',**content)
        else:
            return '未找到相关货物信息！（no information with serial number : %s）'%nbr

@app.route('/goodcode/<int:nbr>/',methods=['GET','POST'])
def goodinfobycode(nbr):
    if request.method == 'GET':
        filters = {}
        filters['goodcode'] = nbr
        res = mysql_get_info(table_Goodinfo, filters)
        if res:
            content = res[0].to_dict()
            print('kkklll')
            print(content)
            return render_template('goodsinfo.html',**content)
        else:
            return '未找到相关货物信息！（no information with serial number : %s）'%nbr
    elif request.method == 'POST':
        req = request.form.to_dict()
        amount = req.get('buyamount',None)
        if not g.user:
            return  redirect('login',)
        if not amount or not amount.isdigit():
            return '请输入正确的购买数量！！！！pls input the right number to buy !!'
        resp = MyCart_handel(g.user, nbr, amount)
        nbr_1 = nbr
        url = url_for('goodinfobycode',nbr = nbr_1)
        if resp.get('status'):
            return render_template('replyaddmycart.html',**{'resp':resp.get('info'),'url':url,})
        else:
            return render_template('replyaddmycart.html',**{'resp':resp.get('info'),'url':url,})
@app.route('/goodsoverview/',methods=['GET','POST'])
def goodsoverview():
    limit = 20
    filters = {'ishaspic':1,'GoodsType':'hair'}
    total_count = mysql_get_count_info(**filters)
    if request.method == 'GET':
        offset = 0
        rs = mysql_get_info_limit(table_Goodinfo,limit,offset,**filters)
        rs = [rs[i:i + 5] for i in range(0, len(rs), 5)]
        return render_template('goodsoverview.html',**{'resgoods':rs,'limit':limit,'offset':offset,'total_count':total_count,'currentpage':1,'GoodType':'all'})
    else:
        offset = 0
        res = request.form.to_dict()
        is_changetype = res.get('is_changetype',None)
        GoodsType = res.get('GoodsType',None)
        currentpage  = res.get('currentpage',None)
        if GoodsType == 'all':
            filters = {'ishaspic': 1,'GoodsType': 'hair'}
        else:
            filters = {'ishaspic': 1, 'GoodsType': 'hair'}
        if is_changetype:
            total_count = mysql_get_count_info(**filters)
            rs = mysql_get_info_limit(table_Goodinfo, limit, offset, **filters)
            rs = [rs[i:i + 5] for i in range(0, len(rs), 5)]
            xxx = render_template('replygoodsoverview.html',**{'resgoods': rs, 'limit': limit, 'currentpage': currentpage, })
            print('post请求的下一页')
            return json.dumps({'data': xxx, 'maxpics': total_count, 'currentpage': 1, 'GoodType': GoodsType,})
        else:
            try:
                if currentpage.isdigit():
                    offset = int(currentpage)*limit
                else:
                    if currentpage:
                        return '请输入正确的页码格式！！'
            except:
                return '请输入页码！！！'
            print('下一页999')
            offset = int(currentpage)*limit
            print(filters)

            print('okok')
            print(limit)
            print(offset)

            rs = mysql_get_info_limit(table_Goodinfo, limit, offset, **filters)
            print('查询结果')
            for i in rs:
                print(i)
            rs = [rs[i:i + 5] for i in range(0, len(rs), 5)]
            xxx = render_template('replygoodsoverview.html',**{'resgoods': rs, 'limit': limit, 'currentpage': currentpage, })
            print(xxx)
            if not xxx:
                xxx = '未找到相关货物！found no goods'
            return json.dumps({'data': xxx, 'maxpics': total_count, 'currentpage': 1, 'GoodType': GoodsType, 'limit': limit,})
@app.route('/mycart/',methods=['GET','POST'])
@login_required
def mycart():
    if request.method == 'GET':
        filters = {'usr_id':g.user}
        usr_type = g.usr_type
        rs = mysql_get_mycart_execsql(usr_type,filters)
        return render_template('mycart.html',**{'goods':rs})
    elif request.method == 'POST':
        req = request.form.to_dict()
        req = req.get('content',None)
        if req:
            req = eval(req)
            if req:
                maxtry = 3
                while maxtry>0:
                    orderid = str(uuid.uuid4())
                    filters = {'orderid':orderid}
                    rs = mysql_get_info(table_Order, filters)
                    if rs:#
                        maxtry = maxtry -1
                        orderid = 0
                    else:
                        maxtry = 0
                if orderid == 0:
                    return '订单生成失败，请稍后重试！！！'
                try:
                    orderprice_UnitPrice = 0
                    orderprice_EstimatePrice = 0
                    for i in req:#req是货物，现在是要把货物添加到订单里
                        filters = {'usr_id':g.user,}
                        timestp = int(time.time())
                        key_value_dict = {'usr_id': g.user,'orderid': orderid,'goodcode':i.get('goodcode'),'amount':i.get('amount'),'timestp':timestp, }

                        goodres = mysql_get_info(table_Goodinfo, {'goodcode':i.get('goodcode')})
                        if goodres:
                            goodprice = goodres[0].UnitPrice
                            goodprice_2 = goodres[0].EstimatePrice
                            orderprice_UnitPrice = orderprice_UnitPrice + int(i.get('amount'))*goodprice
                            orderprice_EstimatePrice = orderprice_EstimatePrice + int(i.get('amount')) * goodprice_2
                            key_value_dict['UnitPrice'] = goodres[0].UnitPrice
                            mysql_add_info(table_Order, key_value_dict)
                    res = mysql_add_info(table_Order_summary, {'usr_id': g.user,'orderid':orderid,'orderprice_UnitPrice':orderprice_UnitPrice,'timestp':timestp,'orderprice_EstimatePrice':orderprice_EstimatePrice})
                    key_value_dict = {'usr_id': g.user}
                    res = mysql_del_info(table_MyCart, key_value_dict)#清空购物车，已经生成订单了
                    #生成订单sumary
                    return "添加成功！！！！"
                except Exception as e:
                    return str(e)
            else:
                return '<h1>购物车为空！！！</h1>'


@app.route('/ordercreate/',methods=['GET','POST'])
@login_required
def ordercreate():
    if request.method == 'GET':
        if g.usr_type == 'admin':
            return render_template('ordercreate.html')
        else:
            return '无权访问！！！'
    else:
        username = request.form['username']
        Turnid = request.form['Turnid']
        if username and Turnid:
            if g.usr_type == 'admin':
                time_str = int(round(time.time() * 1))#10位时间戳
                orderid = str(uuid.uuid4())
                rs = mysql_ordercreate_execsql(username, Turnid,time_str,orderid)
                return rs
            else:

                return '无权访问！！！'


        else:
            return '请填写username 及 turnid！！！'




@app.route('/',methods=['GET'])
def index():
    if request.method == 'GET':
        return redirect("goodsoverview")


@app.route('/tasktodo/',methods=['GET','POST'])
@login_required
def tasktodo():
    if request.method == 'GET':
        filters = {
            'saler' : g.user,
            'issold':0,
        }
        total_count = mysql_get_count_goods_info(**filters)
        return render_template('salesupdate.html',**{'total_count':total_count})
    else:
        req = request.form.to_dict()
        actiontodo = req.get('action',None)
        SoledPrice = req.get('SoledPrice',None)
        SerialNumber = req.get('SerialNumber', None)
        if actiontodo == 'update':
            if not SoledPrice:
                return '请输入SoledPrice！！！'
            elif not SerialNumber:
                return '请输入SerialNumber！！！'
            elif not SoledPrice.isdigit():
                return '请输入整数！！SoledPrice shall be a integer'
            else:
                nbr = req.get('SerialNumber')
                filters = {}
                filters['SerialNumber'] = nbr
                if g.usr_type != 'admin':
                    filters['saler'] = g.user
                else:
                    pass
                print(filters)
                res = mysql_get_info(table_Goods, filters)
                if not res:
                    return "查无此物或货物不属于你，请核查货物串号信息！！！no goods foud,pls double check the SerialNumber"
                else:
                    if int(res[0].issold):
                        return '该货物已记录为“已销售”，请联系管理员解决/goods with this SerialNumber has been soled,pls contact the administrator '
                    else:
                        filters['SoledPrice'] = SoledPrice
                        filters['issold'] = 1
                        print(filters)
                        mysql_update_info(res, filters)
                        return '添加记录成功/update success！'
        else:
            if not SerialNumber:
                return '请输入SerialNumber！！！'
            else:
                nbr = req.get('SerialNumber')
                filters = {}
                filters['SerialNumber'] = nbr
                if g.usr_type != 'admin':
                    filters['saler'] = g.user
                res = mysql_get_info(table_Goods, filters)
                if not res:
                    return_dict = {'status':'nok','info':"查无此物或货物不属于你，请核查货物串号信息！！！no goods foud,pls double check the SerialNumber"}
                    rexx = json.dumps(return_dict)
                    return jsonify(rexx)
                else:
                    res_dict = res[0].to_dict()
                    return_dict = {
                        'status': 'ok',
                        'SerialNumber':res_dict.get('SerialNumber',None),
                        'TurnId': res_dict.get('TurnId', None),
                        'goodcode': res_dict.get('goodcode', None),
                        'Brand': res_dict.get('Brand', None),
                        'Color': res_dict.get('Color', None),
                        'Standards': res_dict.get('Standards', None),
                        'UnitPrice': res_dict.get('UnitPrice', None),
                        'owener': res_dict.get('owener', None),
                        'EstimatePrice': res_dict.get('EstimatePrice', None),
                        'GoodsType': res_dict.get('GoodsType', None),
                        'SoledPrice': res_dict.get('SoledPrice', None),
                        'Pic1Name1': res_dict.get('Pic1Name1', None),
                        'Pic1Name2': res_dict.get('Pic1Name2', None),
                    }
                    rexx = json.dumps(return_dict)
                    return jsonify(rexx)


@app.route('/ordermanager/')
@login_required
def ordermanager():
    filters = {'usr_id': g.user,'isclosed':'0'}
    usr_type = g.usr_type
    rs = mysql_get_order_overview_execsql(usr_type,filters)
    for i in rs:
        print(i)
    return render_template('ordermanager.html',**{'orders': rs})

@app.route('/orderinfo/<uuid:uid>/')
@login_required
def orderinfo(uid):
    if g.usr_type == 'admin':
        filters = {'uid':uid}
    else:
        filters = {'usr_id': g.user,'uid':uid}
    uid = str(uid)
    filters['orderid'] = uid
    rs = mysql_get_order_info_execsql(g.usr_type,filters)
    return render_template('orderinfo.html',**{'orders':rs})


@app.route('/uploads/<filename>/')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route("/getmyapp/", methods=['GET'])
def getmyapp():
    directory = os.getcwd()
    # 此处的filepath是文件的路径，但是文件必须存储在static文件夹下， 比如images\test.jpg
    return send_from_directory(directory, 'myapp.apk', as_attachment=True,attachment_filename='myapp.apk')


@app.route('/hxy/')
def hxy():
    return render_template('hxy.html')

@app.route('/onlineshow/')
def onlineshow():
    return render_template('onlineshow.html')

#112
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=80,threaded=True,)
