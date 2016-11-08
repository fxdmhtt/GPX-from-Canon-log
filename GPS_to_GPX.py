# coding: utf8

import sys

point = {"lat":"", "lon":"", "ele":"", "date":""} # словарь для одной точки

params = sys.argv[1:] # получили параметры командной строки

for param_file in params:
    track = {} # пустой словарь для точек всего трека
    file_name = param_file.split('.')[0] # взяли имя очередного файла без расширения

    file = open(param_file, 'r') # открыли его на чтение
    
    def degmin_to_deg(strDM, sph): # функция переводит из строки формата ггмм.мммм в гг.ггггг в sph - полушарие (N, S, E, W)
        fDM = float(strDM)
        deg = int((fDM/100))
        ddeg = ((fDM/100)%1)*100/60
        deg = deg+ddeg
        if ((sph == 'S') or (sph == 'W')):
            deg = deg * (-1)
        return "%.5F" % deg
    
    for i in file: # цикл построчного разбора файла
        string = i[:-1].split(',')
        if len(string) < 2: continue
        time = int(string[1].split(".")[0])
        if ((time in track) == False):
            track[time] = point.copy()
        if string[0] == '$GPGGA':
            track[time]['ele'] = string[9]
        if string[0] == '$GPRMC':
            track[time]['lat'] = degmin_to_deg(string[3], string[4])
            track[time]['lon'] = degmin_to_deg(string[5], string[6])
            stime = string[1].split('.')[0]
            sdate = string[9]
            date = "20%s-%s-%sT%s:%s:%sZ" % (sdate[4:], sdate[2:4], sdate[:2], stime[:2], stime[2:4], stime[4:])
            track[time]['date'] = date
    
    file.close() # закрыли входой файл за ненадобностью
    
    trkpt = '''
            <trkpt lat="%(lat)s" lon="%(lon)s">
                <time>%(date)s</time>
                <ele>%(ele)s</ele>
            </trkpt>'''
    
    gpx_str = '''<?xml version="1.0" encoding="UTF-8"?>
    <gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0" xmlns="http://www.topografix.com/GPX/1/0" creator="Jogick" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">
        <trk>
            <name>Canon PowerShot SX280 HS</name>
            <trkseg>%s
            </trkseg>
        </trk>
    </gpx>'''
    
    track_string = ''
    
    for i in sorted(track.keys()):
        track_string = track_string + trkpt % (track[i])
    
    gpx = gpx_str % track_string
    
    gpx_file_name = "%s.gpx" % file_name
    gpx_file = open(gpx_file_name, 'w')
    gpx_file.write(gpx)
    gpx_file.close()