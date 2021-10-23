from django.shortcuts import render
import pandas as pd
import psycopg2

# Create your views here.
con = psycopg2.connect(
    host="",
    database="",
    user="",
    password="",
    port="5432"
)

cur = con.cursor()

def home(request):
    return render(request,"upload/index.html")

def upload(request):
    message = ''
    code = 0
    try:
        if request.POST:
            file = request.FILES['file']
            name_file = str(file)
            # ROOT URL - Ruta raiz donde se encuentra el archivo o los archivos.
            df = pd.read_csv(r'ROOT_URL'+ name_file, encoding='latin-1',sep=';')
            df = df.fillna('')
            df = df.to_numpy().tolist()
            lista = list (df)

            tuplaa = tuple(lista)

            cur = con.cursor()

            cur.executemany("INSERT INTO dashboard_powerbi (id,created_at,name_one,name_platform,text_in,text_out,intent_name,session_id,client_phone,phone,name_two,user_name,name_treee,last_name,metadata) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",tuplaa)
            if cur.rowcount == 190:
                con.commit()
                con.close()
                message = 'Carga de archivo exitosa!!'
                code = 1
            else:
                message = 'El archivo no se cargo'
                code = 2
        else:
            message = 'No se reconoce parametros en el metodo POST'
            code = 0
    except:
        message = 'El archivo no tiene el formato correcto o la ubicación raíz es diferente!!'
        code = 0

    return render(request, "upload/result.html", {'message': message,'code':code})
