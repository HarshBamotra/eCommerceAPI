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


################## test function for buyer ##################

@api_view(['GET']) 
def test(request):
    return Response({'Status':'ok', 'Message':'Welcome to the buyer endpoint !!'})


################## function for buyer registration ##################

@api_view(['POST'])
def register(request):
    name = request.data['name']
    email = request.data['email']
    password = request.data['password']
    address = request.data['address']

    try:
        cursor = connection.cursor()
        cursor.execute('''INSERT into buyer (name, email, password, address) values("''' + name + '", "' + email + '", "' + password + '", "' + address + '")')
        return Response({"Message": "Registration  sucessfull."})
    except db.OperationalError as e:
        return Response(list({'Error': e}), status = 400)
    except db.Error as e:
        return Response(list({'Error': e}), status = 400)
    except:
        return Response({'Error': 'Invalid Parameter'}, status = 400)
    


################## function for buyer login ##################

@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']

    try:
        cursor = connection.cursor()
        cursor.execute('''select password from buyer where email = "''' + email + '"')
        passdb = cursor.fetchone()[0]
        print(passdb)
        if(password == passdb):
            token = encode_user({'email':email, 'password':password})
            cursor.execute('''update buyer set token = "''' + token + '" where email = "' + email + '"')
            return Response({"Message": "Login  sucessfull.", "Access Token":token})
        else:
            return Response({"Message": "Wrong Password."}, status=401)
    except db.OperationalError as e:
        return Response(list({'Error': e}), status = 400)
    except db.Error as e:
        return Response(list({'Error': e}), status = 400)
    except:
        return Response({'Error': 'Invalid Parameter'}, status = 400)
    


################## function for buyer logout ##################

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
        cursor.execute('''select password from buyer where email = "''' + email + '"')
        passdb = cursor.fetchone()[0]
        print(passdb)
        if(password == passdb):
            cursor.execute('''update buyer set token = NULL''' + ' where email = "' + email + '"')
            return Response({"Message": "Logout  sucessfull."})
        else:
            return Response({"Message": "Wrong Password."}, status=401)
    except db.OperationalError as e:
        return Response(list({'Error': e}), status = 400)
    except db.Error as e:
        return Response(list({'Error': e}), status = 400)
    except:
        return Response({'Error': 'Invalid Parameter'}, status = 400)
    


################## function to get, updata and delete buyer data ##################

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
            cursor.execute('''SELECT name, email, address FROM buyer where email = "''' + email + '"')
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
            cursor.execute('''delete from buyer where email = "''' + email + '"')
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
        address = request.data['address']
        password = request.data['password']
        try:
            token = request.query_params['token']
            email = decode_user(token)['email']
        except:
            return Response({'Error': 'Access Denied.'}, status = 401)
        try:
            cursor = connection.cursor()
            cursor.execute('''update buyer set name = "''' + name + '", email = "' +  email_new + '", address = "' + address + '", password = "' + password + '" where email = "' + email + '"')
            if(cursor.rowcount == 0):
                return Response({"Message": "User does not exists."}) 
            else:
                return Response({"Message": "Data updated sucessfully."})
        except:    
            return Response({'Error': 'Invalid Parameter'}, status = 400)
        

################## function for buyer to buy a product ##################

@api_view(['POST'])   
def buy(request):
    product = request.data['id']
    try:
        token = request.query_params['token']
        email = decode_user(token)['email']
        password = decode_user(token)['password']
    except:
        return Response({'Error': 'Authentication failed.'}, status = 401)
    try:
        cursor = connection.cursor()
        cursor.execute('''select password from buyer where email = "''' + email + '"')
        passdb = cursor.fetchone()[0]
        cursor.execute('''select id from buyer where email = "''' + email + '"')
        buyer_id = cursor.fetchone()[0]

        cursor.execute('''select seller_id from product where id = "''' + str(product) + '"')
        if(cursor.rowcount == 0):
            return Response({"Message": "Product does not exists."}) 
        else:
            seller_id = cursor.fetchone()[0]
        print(passdb)
        if(password == passdb):
            cursor.execute('''insert into transactions (seller_id, product_id, buyer_id) values("''' + str(seller_id) + '", "' + str(product) + '", "' + str(buyer_id) + '")')
            return Response({"Message": "Purchase sucessfull."})
        else:
            return Response({"Message": "Authentication failed."}, status=401)
    except db.OperationalError as e:
        return Response(list({'Error': e}), status = 400)
    except db.Error as e:
        return Response(list({'Error': e}), status = 400)
    except:
        return Response({'Error': 'Invalid Parameter'}, status = 400)