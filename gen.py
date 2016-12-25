#!/usr/bin/env python3
import cgi
import sys
import codecs
import os

form = cgi.FieldStorage()
filt = form.getlist("obj")
targetID = []
for i in filt:
    targetID.append(int(i))


if targetID == []:
    targetID = list(range(0,100))
#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
#targetID = list(range(0,100))#get from url
MapScript = ""



def getJSmark(Mid, x,y,text,ico):
    text = text.replace("'",r"\'")
    #text = text.replace(r"\n","\n")
    s = ",\n myPlacemark" + str(Mid) + " = new ymaps.Placemark([" + str(x) + ", " + str(y) + "], {\n" 
    #s += "hintContent: '" + text + "',\n"
    s += "balloonContent: '" + text + "'\n" 
    s += "}, {\n" 
    s += "iconLayout: 'default#image',\n"
    s += "iconImageHref: '/images/" + ico + "',\n"
    s += "iconImageSize: [32, 32],\n"
    s += "iconImageOffset: [-16, -16]\n})"
    return s

#Open&Get std marks
def getObjects():
    global targetID
    importFiles = []
    #Main file of mark objects
    obj = open("objects/objects.txt", 'r', encoding='utf-8')
    objs = obj.readlines()
    obj.close()
    for line in objs:
        if line == "\n":
            continue
        data = line.split()
        #Check dataType in target IDs
        if int(data[0]) in targetID:
            #Add
            importFiles.append((data[1],data[2]))
    return importFiles

#Add marks to script
def getMarks():
    global MapScript
    importFiles = getObjects()
    importPoints = []
    for i in importFiles:
        obj = open("objects/" + i[0], 'r', encoding='utf-8')
        objs = obj.readlines()
        obj.close()
        for j in objs:
            data = j.split()
            importPoints.append(int(data[0]))
            MapScript += getJSmark(int(data[0]), float(data[1]), float(data[2]), " ".join(data[3:]), i[1]) + "\n"
        
    MapScript += ";"
    
    for i in importPoints:
        MapScript += "myMap.geoObjects.add(myPlacemark" + str(i) + ");\n"




def getFiltersObj():
    global targetID
    importFiles = []
    #Main file of mark objects
    obj = open("objects/objects.txt", 'r', encoding='utf-8')
    objs = obj.readlines()
    obj.close()
    s = ""
    for i in objs:
        data = i.split()
        if i == '\n':
            continue
        if int(data[0]) in targetID:
            s += '<input id="cb' + data[0]+'" type="checkbox" name="obj" value = "' + data[0] + '" checked>'
        else:
            s += '<input id="cb' + data[0]+'" type="checkbox" name="obj" value = "' + data[0] + '">'
        s += '<img src="../images/' + data[2] + '" style="width:16px;height:16px;" align="top">' + data[3] +  "\n""<Br>" +"\n"
    return s

def Run(name):
    global MapScript
    sys.stdout = open('out\\' + name,'w')
    
    MapScript = """
    ymaps.ready(function () {
        var myMap = new ymaps.Map('map', {
                center: [58.140429, 52.674267],
                zoom: 14,
                controls: []
            }, {
                searchControlProvider: 'yandex#search'
            })
    """
    getMarks()

    #Finalization
    MapScript += "});"
    #sys.exit(0)     
    

    print("""<!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">

    <link rel="shortcut icon" href="../images/ico.ico" type="image/x-icon">

        <title>Glazov map with places</title>
        <script src="//api-maps.yandex.ru/2.1/?lang=en_RU" type="text/javascript"></script>
        
        <script type="text/javascript">
    """)
    print(MapScript)
    print("""
          

        </script>

            <style>
            html, body {
                width: 100%;
                height: 100%;
                padding: 0;
                margin: 0;
            }
                    p, h2{
                            margin: 0px;
                    }
            #map {
                width: 80%;
                height: 100%;
                padding: 0;
                margin: 0;
                float:left;
            }
            #text{
                width: 18%;
                padding: 1%;
                margin: 0;
                float:right;
            }
            #footer {
                position: fixed;
                bottom:0;
                padding: 5px; 
                background: #FFFFFF;
                color: #000000; 
                width: 100%;
           }

        </style>
    </head>
    <body>


    <div id="map" ></div>
    <div id="text" >""")
    print('<form id="sumbitform" action="' + name + '">')
    print("<p><b>Choose the objects</b><Br>")
    print(getFiltersObj())
    #print("<p><b>Choose the polygone</b><Br>")
    #print(getFiltersPoly())
    print("""
          </p>
          <p><input type="submit" value="Submit"></p>
         </form>
             <br>
             
        <div id="footer">
           
           <a href="https://github.com/AsciiShell/GlazovMap">Repository on GitHub</a>
        </div>
    </div>
        <script>
  document.getElementById('cb2').onchange = function() {
    var i = 0;
    var f = document.getElementById('sumbitform');
    var s = f.getAttribute("action");
    if (document.getElementById('cb2').checked)
    {
        s = s.slice(0,i) + "1" + s.slice(i+1);
    }
    else
    {
        s = s.slice(0,i) + "0" + s.slice(i+1);
    }
    f.setAttribute("action",s);
    
  };
   </script>
  <script>
  document.getElementById('cb3').onchange = function() {
    var i = 1;
    var f = document.getElementById('sumbitform');
    var s = f.getAttribute("action");
    if (document.getElementById('cb3').checked)
    {
        s = s.slice(0,i) + "1" + s.slice(i+1);
    }
    else
    {
        s = s.slice(0,i) + "0" + s.slice(i+1);
    }
    f.setAttribute("action",s);
    
  }; 
     </script>
  <script>
   document.getElementById('cb4').onchange = function() {
    var i = 2;
    var f = document.getElementById('sumbitform');
    var s = f.getAttribute("action");
    if (document.getElementById('cb4').checked)
    {
        s = s.slice(0,i) + "1" + s.slice(i+1);
    }
    else
    {
        s = s.slice(0,i) + "0" + s.slice(i+1);
    }
    f.setAttribute("action",s);
    
  };
     </script>
  <script>
    document.getElementById('cb5').onchange = function() {
    var i = 3;
    var f = document.getElementById('sumbitform');
    var s = f.getAttribute("action");
    if (document.getElementById('cb5').checked)
    {
        s = s.slice(0,i) + "1" + s.slice(i+1);
    }
    else
    {
        s = s.slice(0,i) + "0" + s.slice(i+1);
    }
    f.setAttribute("action",s);
    
  };
     </script>
  <script>
    document.getElementById('cb7').onchange = function() {
    var i = 4;
    var f = document.getElementById('sumbitform');
    var s = f.getAttribute("action");
    if (document.getElementById('cb7').checked)
    {
        s = s.slice(0,i) + "1" + s.slice(i+1);
    }
    else
    {
        s = s.slice(0,i) + "0" + s.slice(i+1);
    }
    f.setAttribute("action",s);
    
  }; 
     </script>
  <script>
   document.getElementById('cb6').onchange = function() {
    var i = 5;
    var f = document.getElementById('sumbitform');
    var s = f.getAttribute("action");
    if (document.getElementById('cb6').checked)
    {
        s = s.slice(0,i) + "1" + s.slice(i+1);
    }
    else
    {
        s = s.slice(0,i) + "0" + s.slice(i+1);
    }
    f.setAttribute("action",s);
    
  }; 
     </script>
  <script>
   document.getElementById('cb8').onchange = function() {
    var i = 6;
    var f = document.getElementById('sumbitform');
    var s = f.getAttribute("action");
    if (document.getElementById('cb8').checked)
    {
        s = s.slice(0,i) + "1" + s.slice(i+1);
    }
    else
    {
        s = s.slice(0,i) + "0" + s.slice(i+1);
    }
    f.setAttribute("action",s);
    
  };  
    </script>
  <script>
   document.getElementById('cb9').onchange = function() {
    var i = 7;
    var f = document.getElementById('sumbitform');
    var s = f.getAttribute("action");
    if (document.getElementById('cb9').checked)
    {
        s = s.slice(0,i) + "1" + s.slice(i+1);
    }
    else
    {
        s = s.slice(0,i) + "0" + s.slice(i+1);
    }
    f.setAttribute("action",s);
    
  };
</script>
    </body>
    </html>
    """)
    sys.stdout.close()
    
objids = [2,3,4,5,7,6,8,9]
sumi = 0
for i1 in range(2):
    for i2 in range(2):
        for i3 in range(2):
            for i4 in range(2):
                for i5 in range(2):
                    for i6 in range(2):
                        for i7 in range(2):
                            for i8 in range(2):
                                targetID = []
                                name = ""
                                if i1:
                                    targetID.append(objids[0])
                                    name += "1"
                                else:
                                    name += "0"
                                if i2:
                                    targetID.append(objids[1])
                                    name += "1"
                                else:
                                    name += "0"
                                if i3:
                                    targetID.append(objids[2])
                                    name += "1"
                                else:
                                    name += "0"
                                if i4:
                                    targetID.append(objids[3])
                                    name += "1"
                                else:
                                    name += "0"
                                if i5:
                                    targetID.append(objids[4])
                                    name += "1"
                                else:
                                    name += "0"
                                if i6:
                                    targetID.append(objids[5])
                                    name += "1"
                                else:
                                    name += "0"
                                if i7:
                                    targetID.append(objids[6])
                                    name += "1"
                                else:
                                    name += "0"
                                if i8:
                                    targetID.append(objids[7])
                                    name += "1"
                                else:
                                    name += "0"
                                name += ".html"
                                Run(name)
                                sumi += 1
                                if sumi > 10:
                                    #sys.exit(0)
                                    pass
