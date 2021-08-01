from flask import render_template,request,redirect,flash
from . import server
from .models import RatingForm
import pymongo
from datetime import datetime
import urllib
import json



@server.route('/route', methods=['GET', 'POST'])
def route():
    if server.config["LOGGED"]:
        try:
            connection = pymongo.MongoClient("mongodb://mongodb:27017/mongodb")
            db_m = connection["mongodb"]
            collection = db_m['Report']
            actual_time = datetime.now().strftime('%d/%m/%y %H:%M:%S')
            reports = collection.find({})
            locations = []
            nbr_rep_dep = 0
            nbr_rep_arr =0
            labels = []
            sorts = []
            for report in reports:

                report_time = datetime.strptime(str(report['time']), "%d/%m/%y %H:%M:%S")
                actual_time_c = datetime.strptime(actual_time, "%d/%m/%y %H:%M:%S")
                res = actual_time_c - report_time
                res_minutes = round(int(res.seconds)//60)
                sort = str(report['sort'])
                if res_minutes < 60:
                    labels.append(str("{0} min ago".format(res_minutes)))
                    locations.append(str(report['place_id']))
                    sorts.append(str(report['sort']))

        except:
            print("Exception")
            locations = []
            labels = []
            sorts = []
            nbr_rep_dep = 0
            nbr_rep_arr = 0

        if request.method == 'POST':

            server.config['FROM'] = str(request.form.get('from'))
            server.config['TO'] = str(request.form.get('to'))
        try:
            actual_time = datetime.now().strftime('%d/%m/%y %H:%M:%S')

            connection = pymongo.MongoClient(
                "mongodb://mongodb:27017/mongodb")
            db_m = connection["mongodb"]
            collection = db_m['Report']

            url_dep = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}".format(
                server.config['FROM'], str(server.config["API_SECRET_KEY"]))
            url_dep = url_dep.replace(" ", "")
            geocoding_dep = urllib.request.urlopen(url_dep)
            decoded_geocoding_dep = json.loads(geocoding_dep.read())
            dep_place_id = json.dumps([s['place_id']
                                    for s in decoded_geocoding_dep['results']][0])
            dep_place_id = dep_place_id.replace('"', "")

            url_arr = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}".format(
                server.config['TO'], str(server.config["API_SECRET_KEY"]))
            url_arr = url_arr.replace(" ", "")
            geocoding_arr = urllib.request.urlopen(url_arr)
            decoded_geocoding_arr = json.loads(geocoding_arr.read())
            arr_place_id = json.dumps([s['place_id']
                                        for s in decoded_geocoding_arr['results']][0])
            arr_place_id = arr_place_id.replace('"', "")

            reports_dep = collection.find({'place_id': dep_place_id})
            reports_arr = collection.find({'place_id': arr_place_id})
            
            nbr_rep_dep = 0
            nbr_rep_arr = 0

            for report in reports_dep:

                report_time = datetime.strptime(
                    str(report['time']), "%d/%m/%y %H:%M:%S")
                actual_time_c = datetime.strptime(
                actual_time, "%d/%m/%y %H:%M:%S")
                res = actual_time_c - report_time
                res_minutes = round(int(res.seconds)//60)
                if res_minutes < 60:
                    nbr_rep_dep += 1

            for report in reports_arr:

                report_time = datetime.strptime(
                    str(report['time']), "%d/%m/%y %H:%M:%S")
                actual_time_c = datetime.strptime(
                    actual_time, "%d/%m/%y %H:%M:%S")
                res = actual_time_c - report_time
                res_minutes = round(int(res.seconds)//60)
                if res_minutes < 60:
                    nbr_rep_arr += 1
        except :
            print('Exception')



        source = "https://maps.googleapis.com/maps/api/js?key={0}&libraries=places".format(str(server.config["API_SECRET_KEY"]))
        
        return render_template('route.html',nbr_rep_dep=nbr_rep_dep, nbr_rep_arr=nbr_rep_arr, source=source, From=server.config['FROM'], To=server.config['TO'], locations=locations, len=len(locations), labels=labels, sorts=sorts)
    return redirect('/signin')

@server.route('/profile')
def profile():
    if server.config["LOGGED"]:
        
        try:
            connection = pymongo.MongoClient("mongodb://mongodb:27017/mongodb")
            db_m = connection["mongodb"]
            collection = db_m['User']
            collection_report = db_m['Report']
            count_reports = collection_report.count_documents({'user':server.config['USERNAME'] })
            user = collection.find_one({'username': server.config["USERNAME"]})
            username = user['username']
            karmapoints = user['karmapoints']

            return render_template('profile.html',karmapoints=karmapoints,username=username,count_reports=count_reports)

        except:
            redirect('/error')
    else:

        return redirect('/signin')


@server.route('/')
def base():
    if server.config["LOGGED"]:
        source = "https://maps.googleapis.com/maps/api/js?key={0}&callback=initMap&libraries=&v=weekly".format(
            str(server.config["API_SECRET_KEY"]))
        
        source2 = "https://maps.googleapis.com/maps/api/js?key={0}&libraries=places&callback=initialize".format(
            str(server.config["API_SECRET_KEY"]))

        try:
            connection = pymongo.MongoClient("mongodb://mongodb:27017/mongodb")
            db_m = connection["mongodb"]
            collection = db_m['Report']
            actual_time = datetime.now().strftime('%d/%m/%y %H:%M:%S')
            reports = collection.find({})
            locations = []
            labels = []
            sorts = []
            for report in reports:
                
                
                report_time = datetime.strptime(
                    str(report['time']), "%d/%m/%y %H:%M:%S")
                actual_time_c = datetime.strptime(
                    actual_time, "%d/%m/%y %H:%M:%S")
                res = actual_time_c - report_time
                res_minutes = round(int(res.seconds)//60)
                sort = str(report['sort'])
                if res_minutes < 60:
                    labels.append(str("{0} min ago".format(res_minutes)))
                    locations.append(str(report['place_id']))
                    sorts.append(str(report['sort']))

        except:
            print("Exception")
            locations = []
            labels=[]
            sorts=[]

        return render_template('index.html',source=source,source2=source2,locations=locations,len = len(locations),labels=labels,sorts=sorts)

        
    return redirect('/signin')


@server.route('/error')
def error():
    return render_template('error.html')


@server.route('/rating', methods=['GET', 'POST'])
def rating():
    form_rating = RatingForm()
    connection = pymongo.MongoClient("mongodb://mongodb:27017/mongodb")
    db_m = connection["mongodb"]
    collection = db_m['Line']
    
    line = 'M2'
    try:
        new_rate = collection.find({'line': line})[0]['avg_rate']
        new_rate = str(round(new_rate,2))+"/5"
    except :
        new_rate = 'Be the first to rate it !'
    if request.method == 'POST' and server.config["LOGGED"]:
        
        try:
            if collection.count_documents({'line': line})==0:
                collection.insert({'line': line, 'avg_rate':int(str(request.form.get('rating'))), 'nbr_rates': 1})
            else:
                rate = int(str(request.form.get('rating')))
                actual_value = collection.find({'line': line})[0]['avg_rate']
                collection.update({'line': line}, {'$inc': {'nbr_rates': 1}})
                N = collection.find({'line': line})[0]['nbr_rates']
                collection.update({'line': line}, {'$inc': {'avg_rate': (1/N)*(rate-actual_value)}}) 
            flash('thanks')
            return redirect('/rating')
        except:
            print('exception')
            return redirect('/error')

    return render_template('rating.html', form_rating=form_rating, new_rate=new_rate)





@server.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
            connection = pymongo.MongoClient("mongodb://mongodb:27017/mongodb")
            db_m = connection["mongodb"]
            collection = db_m['User']
            
            dict_new_user = {"username": str(request.form.get('username')),"karmapoints":0, "password": str(request.form.get('password'))}


            try:
                count_documents = collection.count_documents({'username': str(request.form.get('username'))})
                if count_documents >0:
                    return redirect('/signup')
                else :
                    collection.insert(dict_new_user)
                return redirect('/signin')
            except:
                return redirect('/signupko')

    return render_template('signup.html')


@server.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        connection = pymongo.MongoClient("mongodb://mongodb:27017/mongodb")
        db_m = connection["mongodb"]
        collection = db_m['User']
        form_username = str(request.form.get('username'))
        form_password = str(request.form.get('password'))

        try:
            mongo_pwd = collection.find({'username': form_username})[0]['password']
        except:
            mongo_pwd=''

        try:
            if mongo_pwd == form_password:
                server.config["LOGGED"] = True
                server.config["USERNAME"] = form_username
                return redirect('/')
            else:
                flash('Wrong password')
                return redirect('/signin')
            
        except:
        
            return redirect('/signupko')

    return render_template('signin.html')


@server.route('/signupko', methods=['GET', 'POST'])
def signupko():
    return render_template('signupko.html')


@server.route('/logout', methods=['GET', 'POST'])
def logout():
    server.config["LOGGED"] = False
    server.config["USERNAME"] = ''
    server.config['FROM'] = ''
    server.config['TO'] = ''
    return redirect('/')


@server.route('/report', methods=['GET', 'POST'])
def report():
    source = "https://maps.googleapis.com/maps/api/js?key={0}&libraries=places".format(
        str(server.config["API_SECRET_KEY"]))
    if request.method == 'POST' and server.config["LOGGED"]:
        connection = pymongo.MongoClient("mongodb://mongodb:27017/mongodb")
        db_m = connection["mongodb"]
        collection = db_m['Report']
        collection_user = db_m['User']
        
        
        try:
            time = datetime.now().strftime("%d/%m/%y %H:%M:%S")
            place = str(request.form.get('place'))
            sort = str(request.form.get('sort'))
            url = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}".format(place, str(server.config["API_SECRET_KEY"]))
            url = url.replace(" ", "")
            geocoding = urllib.request.urlopen(url)
            decoded_geocoding = json.loads(geocoding.read())
            place_id = json.dumps([s['place_id'] for s in decoded_geocoding['results']][0])
            place_id = place_id.replace('"',"")
            dict_new_report = {"report": str(request.form.get('report')), "place_id": place_id, "time": time, "user": server.config["USERNAME"],"sort":sort}
            if str(request.form.get('report')) != '':
                collection.insert(dict_new_report)
                collection_user.update_one({'username': server.config["USERNAME"]}, {'$inc': {'karmapoints': 50}}, upsert=True)
                flash("Thanks")
                return redirect('/')
            else:
                return redirect('/report')
        except:
            flash("Problem")
            return redirect('/report')
        

    return render_template('report.html',source=source)
