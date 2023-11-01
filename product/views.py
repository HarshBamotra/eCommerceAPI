from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connection
import django.db as db


################## function to get all the products  ##################

@api_view(['GET'])
def getall(request):
    try:
        cursor = connection.cursor()
        cursor.execute('''select * from product''')
        if cursor.rowcount == 0:
            return Response({"Message": "Products not found."}, status=404)
        else:
            result = cursor.fetchall()
            return Response(result)
    except db.OperationalError as e:
        return Response(list({'Error': e}), status = 400)
    except db.Error as e:
        return Response(list({'Error': e}), status = 400)
    except:
        return Response({'Error': 'Invalid Parameter'}, status = 400)
    



################## function to get a product by id  ##################

@api_view(['GET'])
def product(request):
    try:
        id = request.query_params['id']
    except:
        return Response({"Error": "Missing parameters."}, status=404)
    try:
        cursor = connection.cursor()
        cursor.execute('''select * from product where id = ''' + str(id) + '"')
        if cursor.rowcount == 0:
            return Response({"Message": "Products not found."}, status=404)
        else:
            result = cursor.fetchone()
            return Response(result)
    except db.OperationalError as e:
        return Response(list({'Error': e}), status = 400)
    except db.Error as e:
        return Response(list({'Error': e}), status = 400)
    except:
        return Response({'Error': 'Invalid Parameter'}, status = 400)