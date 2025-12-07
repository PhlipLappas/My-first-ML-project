from sklearn.tree import DecisionTreeRegressor
import csv
import numpy as np
import random


sheets = []
price = []

#Χρώματα  
prasino = 1
menta = 2
mpez = 3
lila = 4
grey = 5 

#CSV file
try:
    with open("sheet_data.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            width = int(row[0])
            length = int(row[1])
            color = int(row[2])
            price_value = float(row[3])
            sheets.append([width, length, color])
            price.append(price_value)
    sheets = np.array(sheets)
    price = np.array(price)
except FileNotFoundError:
    sheets = np.array([ 
        [230,260,1], [270,260,3], [170,260,3],
        [230,260,3], [270,260,4], [170,260,4],
        [230,260,4], [270,260,1], [170,260,1],
        [230,260,5],
    ])
    price = np.array([ 
        35.91, 40.50, 26.91, 35.91, 40.50,
        26.91, 35.91, 40.50, 26.91, 35.91,
    ])
new_orders_to_save = []
rec_sheets = []
rec_price = []
try:
    with open("rec_data.csv","r")as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row)>=4:
                try:
                    rec_width = int(row[0])
                    rec_length = int(row[1])
                    rec_color = int(row[2])
                    price_value = float(row[3])
                    rec_sheets.append([rec_width,rec_length,rec_color])
                    rec_price.append(price_value)
                except:
                    continue

    rec_sheets = np.array(rec_sheets)
    rec_prices = np.array(rec_price)
except FileNotFoundError:
    pass    

new_recommendations_to_save = []

#Επιλογές χρωμάτων
print("=" * 50)
print("ΕΠΙΛΟΓΕΣ ΧΡΩΜΑΤΩΝ:")
print("1. Πράσινο")
print("2. Μέντα") 
print("3. Μπεζ")
print("4. Λίλα")
print("5. Γκρι")
print("=" * 50)
valid_colors = ['πράσινο', 'μέντα', 'μπεζ', 'λιλά', 'γκρι']
color_mapping = {
    1: "Πράσινο",
    2: "Μέντα",
    3: "Μπεζ",
    4: "Λιλά",
    5: "Γκρι"
}

#Προτάσεις
def recommend(color_code, width, length):
    best = []
    for sheet in sheets:
        score = 0
        if sheet[2] == color_code:
            score += 2  
        if sheet[0]- width == 0 and sheet[1]-length ==0:
            score = score - 1
        elif abs(sheet[0] - width) < 20:
            score += 1
        if abs(sheet[1] - length) < 20:
            score += 1
        best.append((score, sheet))
    best.sort(reverse=True, key=lambda x: x[0])
    return best[:2]  

#AI Model
model = DecisionTreeRegressor()
model.fit(sheets, price)

#Παραγγελία
print("Γεια σας καλοσωρίσατε στο ΛΑΠ Home-Λευκά Είδη")
print("Πληκτρολογίστε για να βρείτε το σεντόνι που ψάχνετε στις καλύτερες τιμές της αγοράς")
orders = int(input('\nΠόσα σεντόνια θέλετε να αγοράσετε; '))
sub_total = 0
recommendations_temp = []
if orders >= 1:
    for i in range(orders):
        print(f"\n--- Σεντόνι {i+1} ---")
        width = int(input('Τι φάρδος θέλετε να έχει το σεντόνι σας; '))
        length = int(input('Τι μάκρος θέλετε να έχει το σεντόνι σας; '))
        
        
        color_input = input('Τι χρώμα θέλετε να είναι το σεντόνι σας; ').lower()
        while color_input not in valid_colors:
            print("❌ Λάθος χρώμα! Διαθέσιμα:", ", ".join(valid_colors))
            color_input = input('Τι χρώμα θέλετε να είναι το σεντόνι σας; ').lower()
        
        
        if color_input == 'πράσινο':
            color_code = 1
        elif color_input == 'μέντα':
            color_code = 2
        elif color_input == 'μπεζ':
            color_code = 3
        elif color_input == 'λιλά':
            color_code = 4
        else:
            color_code = 5

        prediction = model.predict([[width, length, color_code]])
        single_price = prediction[0]
        sub_total += single_price
        print(f"💰 Τιμή σεντονιού: {single_price:.2f} €")
        new_orders_to_save.append([width, length, color_code, single_price]) #Αποθήκευση παραγγελίας μέσα στο CSV file 
        
        recs = recommend(color_code, width, length)  
        recommendations_temp.append(recs)
        for score, item in recs:
            rec_width, rec_length, rec_color = item
            rec_price = model.predict([[rec_width, rec_length, rec_color]])[0]
            new_recommendations_to_save.append([rec_width, rec_length, rec_color, rec_price])


        
#Ενδιαφέρον Προϊόντα  
print("\n🎯 Μπορεί επίσης να σας ενδιαφέρουν:")
for recommendation_set in recommendations_temp:
    for score, item in recommendation_set:
        rec_width, rec_length, rec_color = item
        
        print(f"- {rec_width}x{rec_length}cm σε χρώμα {color_mapping[rec_color]}")
#Επιπρόσθετα προϊόντα
n = input("Θέλετε νά προσθέσετε κάτι στην παραγγελία σας;")
while n.lower() not in ["όχι", "oxι", "no", "οχι"]:
   orders = int(input('\nΠόσα σεντόνια θέλετε να προσθέσετε; '))
   sub_total += 0
   recommendations_keep = []
   if orders >= 1:
    for i in range(orders):
        print(f"\n--- Σεντόνι {i+1} ---")
        width = int(input('Τι φάρδος θέλετε να έχει το σεντόνι σας; '))
        length = int(input('Τι μάκρος θέλετε να έχει το σεντόνι σας; '))
        color_input = input('Τι χρώμα θέλετε να είναι το σεντόνι σας; ').lower()
        while color_input not in valid_colors:
            print("❌ Λάθος χρώμα! Διαθέσιμα:", ", ".join(valid_colors))
            color_input = input('Τι χρώμα θέλετε να είναι το σεντόνι σας; ').lower()
        current_order = 0
        
        if color_input == 'πράσινο':
            color_code = 1
        elif color_input == 'μέντα':
            color_code = 2
        elif color_input == 'μπεζ':
            color_code = 3
        elif color_input == 'λιλά':
            color_code = 4
        else:
            color_code = 5
        all_recs_tuples = []
        for recommendation_set in recommendations_temp:
            for score, item in recommendation_set:
                rec_tuple = (item[0], item[1], item[2])  
                all_recs_tuples.append(rec_tuple)
        current_tuple = (width,length,color_code)
        if current_tuple in all_recs_tuples:
            print("🎯 Αυτό ήτανε μια από τις προτάσεις μας")
            with open('rec_data.csv', 'a') as f:
                for rec in new_recommendations_to_save:
                    if(rec[0],rec[1],rec[2]) == current_tuple:
            
                        rec_width , rec_length , rec_color,rec_price = rec
                        f.write(f"{rec_width},{rec_length},{rec_color},{rec_price}\n")    
                   

        prediction = model.predict([[width, length, color_code]])
        single_price = prediction[0]
        sub_total += single_price
        print(f"💰 Τιμή σεντονιού: {single_price:.2f} €")
        new_orders_to_save.append([width, length, color_code, single_price]) #Αποθήκευση παραγγελίας μέσα στο CSV file
        recs = recommend(color_code, width, length)  
        recommendations_keep.append(recs)
        for score, item in recs:
            rec_width, rec_length, rec_color = item
            rec_price = model.predict([[rec_width, rec_length, rec_color]])[0]
            new_recommendations_to_save.append([rec_width, rec_length, rec_color, rec_price])
        #Ενδιαφέρον Προϊόντα  
        print("\n🎯 Μπορεί επίσης να σας ενδιαφέρουν:")
        for recommendation_set in recommendations_keep:
            for score, item in recommendation_set:
                rec_width, rec_length, rec_color = item
                print(f"- {rec_width}x{rec_length}cm σε χρώμα {color_mapping[rec_color]}")
   n = input("Θέλετε νά προσθέσετε κάτι στην παραγγελία σας;")
with open("data.csv", "a") as f:
        for order in new_orders_to_save:
         f.write(f"{order[0]},{order[1]},{order[2]},{order[3]}\n")

#Σύνολικο ποσό
print(f'\n💰 Σύνολο παραγγελίας: {sub_total:.2f}€')

#Εκπτώση
p = 0
if sub_total > 80:
    p = 1
    sub_total2 = sub_total - (0.10 * sub_total)
    print('🎉 Έκπτωση 10%!')
    print(f'💰 Τελικό κόστος με έκπτωση: {sub_total2:.2f}€')
final_amount = sub_total2 if p == 1 else sub_total

#πληρώμη       
print('\n' + '=' * 50)
print('💳 ΕΠΙΛΟΓΕΣ ΠΛΗΡΩΜΗΣ')
print('=' * 50)
print('[1] Μια πληρωμή')
print('[2] 3 άτοκες δόσεις')
print('[3] 6 άτοκες δόσεις')
payment = input('\n👉 Επιλογή πληρωμής (1/2/3): ')
if payment == "1":
    print(f'✅ Μια πληρωμή: {final_amount:.2f}€')
elif payment == "2":
    monthly = final_amount / 3
    print(f'✅ 3 άτοκες δόσεις: {monthly:.2f}€/μήνα για 3 μήνες')
else:
    monthly = final_amount / 6
    print(f'✅ 6 άτοκες δόσεις: {monthly:.2f}€/μήνα για 6 μήνες')

#Κωδικός επιβεβαίωσης
print('\n🔐 ΕΠΙΒΕΒΑΙΩΣΗ ΠΑΡΑΓΓΕΛΙΑΣ')
passcode = random.randint(1000, 9999)
print(f"Ο κωδικός επιβεβαίωσης είναι: {passcode}")
verify = input("Εισάγετε τον κωδικό: ")
if verify == str(passcode):
    print("✅ Η παραγγελία ΕΠΙΒΕΒΑΙΩΘΗΚΕ!")
    print("📦 Τα προϊόντα σας ετοιμάζονται για αποστολή!")
else:
    print("❌ Λάθος κωδικός! Η παραγγελία ακυρώθηκε")

#Κλέισιμο
print('\n🎉 Ευχαριστούμε που επιλέξατε την ΛΑΠ Home!')
print('⭐ Σας περιμένουμε ξανά!')
