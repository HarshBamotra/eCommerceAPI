from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connection
import django.db as db
import jwt

################## function to encode jwt token ##################

def encode_user(payload):
    encoded_data = jwt.encode(payload, key='secret',algorithm="HS256")
    return encoded_data

################## function to encode jwt token ##################

def decode_user(token: str):
    decoded_data = jwt.decode(jwt=token,key='secret',algorithms=["HS256"])
    return decoded_data


################## test function for seller ##################

@api_view(['GET']) 
def test(request):
    return Response({'Status':'ok', 'Message':'Welcome to the seller endpoint !!'})


################## function for seller registration ##################

@api_view(['POST'])
def register(request):
    name = request.data['name']
    email = request.data['email']
    password = request.data['password']

    try:
        cursor = connection.cursor()
        cursor.execute('''INSERT into seller (name, email, password) values("''' + name + '", "' + email + '", "' + password + '")')
        return Response({"Message": "Registration  sucessfull."})
    except db.OperationalError as e:
        return Response(list({'Error': e}), status = 400)
    except db.Error as e:
        return Response(list({'Error': e}), status = 400)
    except:
        return Response({'Error': 'Invalid Parameter'}, status = 400)
    


################## function for seller login ##################

@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']

    try:
        cursor = connection.cursor()
        cursor.execute('''select password from seller where email = "''' + email + '"')
        passdb = cursor.fetchone()[0]
        print(passdb)
        if(password == passdb):
            token = encode_user({'email':email, 'password':password})
            cursor.execute('''update seller set token = "''' + token + '" where email = "' + email + '"')
            return Response({"Message": "Login  sucessfull.", "Access Token":token})
        else:
            return Response({"Message": "Wrong Password."}, status=401)
    except db.OperationalError as e:
        return Response(list({'Error': e}), status = 400)
    except db.Error as e:
        return Response(list({'Error': e}), status = 400)
    except:
        return Response({'Error': 'Invalid Parameter'}, status = 400)
    


################## function for seller logout ##################

@api_view(['GET'])
def logout(request):
    try:
        token = request.query_params['token']
        email = decode_user(token)['email']
        password = decode_user(token)['password']
    except:
        return Response({'Error': 'Access Denied.'}, status = 401)
    
    try:
        cursor = connection.cursor()
        cursor.execute('''select password from seller where email = "''' + email + '"')
        passdb = cursor.fetchone()[0]
        print(passdb)
        if(password == passdb):
            cursor.execute('''update seller set token = NULL''' + ' where email = "' + email + '"')
            return Response({"Message": "Logout  sucessfull."})
        else:
            return Response({"Message": "Wrong Password."}, status=401)
    except db.OperationalError as e:
        return Response(list({'Error': e}), status = 400)
    except db.Error as e:
        return Response(list({'Error': e}), status = 400)
    except:
        return Response({'Error': 'Invalid Parameter'}, status = 400)
    


################## function to get, update and delete seller data ##################

@api_view(['GET', 'PUT', 'DELETE'])
def me(request):
    if(request.method == 'GET'):
        try:
            token = request.query_params['token']
            email = decode_user(token)['email']
        except:
            return Response({'Error': 'Access Denied.'}, status = 401)
        try:
            cursor = connection.cursor()
            cursor.execute('''SELECT name, email FROM seller where email = "''' + email + '"')
            result = cursor.fetchone()
            if(result):
                return Response(result)
            else:
                return Response({'Error': 'User does not exist.'}, status = 404)
        except:    
            return Response({'Error': 'Invalid Parameter'}, status = 400)
        
    elif(request.method == 'DELETE'):
        try:
            token = request.query_params['token']
            email = decode_user(token)['email']
        except:
            return Response({'Error': 'Access Denied.'}, status = 401)
        try:
            cursor = connection.cursor()
            cursor.execute('''delete from seller where email = "''' + email + '"')
            if(cursor.rowcount == 0):
                return Response({"Message": "User does not exists."}) 
            else:
                return Response({"Message": "User deleted sucessfully."})
        except db.OperationalError as e:
            return Response(list({'Error': e}), status = 400)
        except db.Error as e:
            return Response(list({'Error': e}), status = 400)
        except:    
            return Response({'Error': 'Invalid Parameter'}, status = 400)   
        
    elif(request.method == 'PUT'):
        name = request.data['name']
        email_new = request.data['email']
        password = request.data['password']
        try:
            token = request.query_params['token']
            email = decode_user(token)['email']
        except:
            return Response({'Error': 'Access Denied.'}, status = 401)
        try:
            cursor = connection.cursor()
            cursor.execute('''update seller set name = "''' + name + '", email = "' +  email_new  + '", password = "' + password + '" where email = "' + email + '"')
            if(cursor.rowcount == 0):
                return Response({"Message": "User does not exists."}) 
            else:
                return Response({"Message": "Data updated sucessfully."})
        except:    
            return Response({'Error': 'Invalid Parameter'}, status = 400)
        

        
        
################## function for seller to add/get products ##################

@api_view(['GET', 'POST']) #get all products from the added by the seller
def products(request):
    if(request.method == 'GET'):
        try:
            token = request.query_params['token']
            email = decode_user(token)['email']
        except:
            return Response({'Error': 'Access Denied.'}, status = 401)
        try:
            cursor = connection.cursor()
            cursor.execute('''SELECT * FROM product where seller_id = (select id from seller where email = "''' + email + '")')
            result = cursor.fetchall()
            if(result):
                return Response(result)
            else:
                return Response({'Error': 'Product does not exist.'}, status = 404)
        except:    
            return Response({'Error': 'Invalid Parameter'}, status = 400)
        
    elif(request.method == 'POST'): #add a new product 
        try:
            token = request.query_params['token']
            email = decode_user(token)['email']
        except:
            return Response({'Error': 'Access Denied.'}, status = 401)
        try:
            name = request.data['name']
            desc = request.data['description']
            category = request.data['category']
            price = request.data['price']
        except:
            return Response({'Error': 'Please provide complete product data.'}, status = 400) 
        try:  
            cursor = connection.cursor()
            cursor.execute('''select id from seller where email = "''' + email + '"')
            seller_id = str(cursor.fetchone()[0])
            cursor.execute('''INSERT into product (item_name, description, category, price, seller_id) values("''' + name + '", "' + desc + '", "' + category + '", "' + str(price) + '", "' + seller_id  + '")')
            return Response({"Message": "Product added sucessfully."})
        except db.OperationalError as e:
            return Response(list({'Error': e}), status = 400)
        except db.Error as e:
            return Response(list({'Error': e}), status = 400)
        except:    
            return Response({'Error': 'Invalid Parameter'}, status = 400)   




################## function for seller to manage added products ##################

@api_view(['PUT', 'POST'])
def product(request):  
    if(request.method == 'POST'): #delete a product by id
        try:
            token = request.query_params['token']
            email = decode_user(token)['email']
        except:
            return Response({'Error': 'Access Denied.'}, status = 401)
        try:
            id = request.data['id']
        except:
            return Response({'Error': 'Missing parameter.'}, status = 400)
        try:
            cursor = connection.cursor()
            cursor.execute('''delete from product where id = "''' + str(id) + '"')
            if(cursor.rowcount == 0):
                return Response({"Message": "Product does not exists."}) 
            else:
                return Response({"Message": "Product deleted sucessfully."})
        except db.OperationalError as e:
            return Response(list({'Error': e}), status = 400)
        except db.Error as e:
            return Response(list({'Error': e}), status = 400)
        except:    
            return Response({'Error': 'Invalid Parameter'}, status = 400)   
        
    elif(request.method == 'PUT'): #update a product by id
        try:
            token = request.query_params['token']
            email = decode_user(token)['email']
        except:
            return Response({'Error': 'Access Denied.'}, status = 401)
        try:
            id = request.data['id']
            name = request.data['name']
            desc = request.data['description']
            category = request.data['category']
            price = request.data['price']
        except:
            return Response({'Error': 'Missing parameter.'}, status = 400)
        try:
            cursor = connection.cursor()
            cursor.execute('''update product set item_name = "''' + name + '", description = "' +  desc  + '", category = "' + category + '", price = "' + str(price) + '" where id = "' + str(id) + '"')
            if(cursor.rowcount == 0):
                return Response({"Message": "Product does not exists."}) 
            else:
                return Response({"Message": "Data updated sucessfully."})
        except:    
            return Response({'Error': 'Invalid Parameter'}, status = 400)