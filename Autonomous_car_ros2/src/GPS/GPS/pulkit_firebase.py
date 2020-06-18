from firebase import firebase
from datetime import datetime
now = datetime.now()
firebase = firebase.FirebaseApplication('https://bluetoothnano-99a9a.firebaseio.com/', None)
fruit_name=input("Enter the name of the fruit :")
fruit_weight=int(input("Enter the name of the fruit :"))
data={'Fruit_name':fruit_name,
      'weight':fruit_weight,
      'time':now
      }
      
      
result=firebase.post('database',data)
print(result)      