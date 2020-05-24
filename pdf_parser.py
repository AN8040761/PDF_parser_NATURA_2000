from tika import parser
from os.path import isfile, join
import glob
import re
files_no_ext = [".".join(f.split(".")[:-1]) for f in glob.glob("*.pdf") if isfile(f)]
files_no_ext.sort() 
print(files_no_ext[0])

def scrap_file(t):
    
    file_name = t + '.pdf'
    path = './' + file_name
    raw = parser.from_file(path)
    text = raw['content']
    #print(text)
    regex_ai = 'Относно: (.*)УВАЖ'
    match_ai = re.findall(regex_ai, text, flags=re.DOTALL)
    match_ai = ''.join(match_ai).replace('\n','') if match_ai else ""
    
    match_a = re.search("имот №\d+", match_ai)
    match_a = match_a.group(0) if match_a else ""
    match_w = re.search("(община|общ\.) ([^,]+)", match_ai)
    match_w = match_w.group(2) if match_w else ""
    match_x = re.search("землището на (с\.|село)", match_ai)
    match_x = "село" if match_x else ""
    match_y = re.search("землището на (с\.|село) ([^,]+)", match_ai)
    match_y = match_y.group(2) if match_y else ""
    match_aj = re.search("ДО.{0,5}(г-жа|г-н|инж\.)? (\w+) (\w+ )?(\w+)", text, re.IGNORECASE | re.DOTALL)
    match_aj = match_aj.group(2) + " " + match_aj.group(4) if match_aj else ""
    regex_ay = 'ДИРЕКТОР.*(\d{2}\.\d{2}\.\d{2,4}).*\Z'
    match_ay = re.findall(regex_ay, text, flags=re.DOTALL)
    match_ay = ''.join(match_ay).replace('.','/')
    match_ax = re.sub(r' ', '', t)
    print("data :" + str(match_ay))
    print("Otnosno: " + match_ai)
    print("imot nom:" + match_a)
    print("data :" + match_ay)
    line_out = match_a + ',' + match_w + ',' + match_x + ',' + match_y + ',"' + match_ai + '",' + match_aj + ',' + match_ax + ',' + match_ay + '\r\n'
    print(line_out)
    with open('out.csv', 'a') as f:
        f.write(line_out)  # Python 3.x

for t in files_no_ext:
    scrap_file(t)


