import time,base64
class admin:
    def __init__(self):
        while True:
            print('********************************************************')
            print("""\t\t1.Add Doctor
                2.Display
                3.Exit""")
            print('********************************************************')
            choice=input("Enter choice:")
            if choice == "1":
                self.add()
            elif choice == "2":
                self.display()
            elif choice == '3':
                break
            else:
                print('invalid choice')
    def add(self):
        print('*** Add Doctor Records ***')
        name=input("Enter Doctor name:")
        spal=input("Enter Specialization:")
        cost=input("Enter Doctor fee:")
        pas=input("Enter New Password:")
        with open("doctor.txt") as f:
            l=len(f.readlines())
            a=l+1
        docid="d00"+str(a)
        with open("doctor.txt","a") as f:
            f.write(f"{docid}|{name}|{spal}|{cost}\n")
        with open("doctor_credential.txt","a") as pf:
            new_pas=encode(pas)
            pf.write(f"{docid}|{new_pas}\n")
        print(f'added new Record Doctor ID:{docid}')
    def display(self):
        count=0
        with open("doctor.txt") as f:
            for i in f.readlines():
                a=i.split('|')
                print(f'Doctor ID:{a[0]}\nDoctor Name:{a[1]}\nDoctor Specialization:{a[2]}\nDoctor fee{a[3]}')
                count+=1
        print(f"Total Record:{count}")
class doctor:
    def __init__(self):
        print('********************************************************')
        self.docid=input("Enter Doctor Id:")
        passwd=input("Enter Password:")
        with open("doctor_credential.txt") as f:
            for i in f.readlines():
                id,pas=i.split('|')
                if self.docid == id and passwd == decode(pas.split("\n")[0]):
                    self.run()
                    break
            else:
                print("Not Found")
    def run(self):
        while True:
            self.ids=[]
            self.ids1=[]
            self.doc=[]
            self.data=("Patient Problem","Patient Bill")
            with open("appointment.txt") as f:
                for i in f.readlines():
                    self.ids.append(i.split("|")[0])
                    self.doc.append(i.split('|')[-1].split('\n')[0])
            with open("save.txt") as f:
                for i in f.readlines():
                    self.ids1.append(i.split("|")[0])
            print('********************************************************')
            print('''\t\t1.Add record
                2.Edit record
                3.Delete record
                4.Search record
                5.Display record
                6.Appointment
                7.Exit''')
            print('********************************************************')
            choice = int(input("Enter Choice:"))
            options={1:self.add,2:self.modify,3:self.delete,4:self.search,5:self.display,6:self.appointment}
            if choice == 7:
                break
            elif choice > 7:
                print('Invalid choice')
            elif choice < 7:
                options[choice]()
    def add(self):
        print('******* Add Patient Records *******')
        n=input('How many records to add:')
        for i in range(1,int(n)+1):
            print(f'\nEnter Patient {i} Record')
            with open('save.txt','a') as f:
                data=[]
                data1=[]
                id=input('Enter Patient Id:')
                if id not in self.ids:
                    print(f'Patient Id {id} do not have new appointment')
                    break
                else:
                    with open('patient.txt') as pf:
                        for i in pf.readlines():
                            if id == i.split('|')[0]:
                                for j in i.split('|'):
                                    data.append(j.split('\n')[0])
                    with open("appointment.txt") as rf:
                        for i in rf.readlines():
                            if id == i.split("|")[0]:
                                continue
                            else:
                                data1.append(i)
                    with open("appointment.txt","w") as wf:
                        for i in data1:
                            wf.write(i)
                    for i in self.data:  
                        data.append(input(f"Enter {i}:"))
                    data.append(self.docid)
                    f.write(f"{'|'.join(data)}\n")
                    print('Added Successfully')
    def modify(self):
        id=input('Enter Patient Id:')
        modify_value=[]
        data=[]
        if id in self.ids1:
            with open('save.txt') as f:
                for i in f.readlines():
                        if id == i.split('|')[0]:
                            with open('modify.txt','a') as mf:
                                mf.write(i)
                        else:
                            modify_value.append(i)
            with open('patient.txt') as pf:
                for i in pf.readlines():
                    if id == i.split('|')[0]:
                        for j in i.split('|'):
                            data.append(j.split('\n')[0])
            for i in self.data:
                data.append(input(f"Enter {i}:"))
            data.append(self.docid)
            modify_value.append(f"{'|'.join(data)}\n")
            with open('save.txt','w') as f:
                modify_value.sort()
                for i in modify_value:
                    f.write(i)
            print("Successfully Modified")
        else:
            print('Patient Id not found!')
    def delete(self):
        saves=[]
        count=0
        id=input('Enter Patient Id:')
        if id in self.ids1:
            with open('save.txt') as sf:
                for i in sf.readlines():
                    if self.docid == i.split('|')[-1].split('\n')[0]:
                        with open('delete.txt','a') as df:
                            df.write(i)
                            count+=1
                        continue
                    else:
                        saves.append(i)
            with open('save.txt','w') as f:
                f.writelines("")
            with open('save.txt','a') as f:
                for i in saves:
                    f.write(i)  
            if count <= 0:
                print('Patient Id not found')
            elif count > 0:
                print(f"Deleted Patient Id:{id}") 
        else:
            print(f'Patient Id {id} not found!')
    def search(self):
        id=input('Enter Patient Id:')
        with open('save.txt') as f:
                for i,j in enumerate(f):
                    v=j.split('|')
                    if v[0] == id and self.docid == v[-1].split('\n')[0]:
                        print(f'Patient Id:{v[0]}\nPatient Name:{v[1]}\nPatient Age:{v[2]}')
                        print(f"Patient Gender:{v[3]}\nPatient Contact:{v[4]}\nPatient Email:{v[5]}")
                        print(f"Patient Address:{v[6]}\nPatient Problem:{v[7]}\nBill:{v[8]}")
                        break
                else:
                    print('Patient Id not found!')
    def display(self):
        count=0
        with open('save.txt') as df:
            for i in df.readlines():
                if self.docid == i.split("|")[-1].split("\n")[0]:
                    v=i.split('|')
                    print(f'Patient Id:{v[0]}\nPatient Name:{v[1]}\nPatient Age:{v[2]}')
                    print(f"Patient Gender:{v[3]}\nPatient Contact:{v[4]}\nPatient Email:{v[5]}")
                    print(f"Patient Address:{v[6]}\nPatient Problem:{v[7]}\nBill:{v[8]}\n")
                    count+=1
            print(f'Total Record:{count}')
            if count == 0:
                print("No Record!")
    def appointment(self):
        with open("appointment.txt") as af:
            for i in af.readlines():
                if self.docid == i.split('|')[1]:
                    v=i.split('|')
                    print(f'Patient Id:{v[0]}\nDoctor Id:{v[1]}\nAppointment Date:{v[2]}\nPatient Problem:{v[3]}\n')
                    break
            else:
                print('No Appointment')
class patient:
    def __init__(self):
        while True:
            print('********************************************************')
            print('''\t\t1.Login
                2.Register
                3.Exit''')
            print('********************************************************')
            choice = input("Enter choice:")
            if choice == "1":
                self.login()
            elif choice == "2":
                self.register()
            elif choice == "3":
                break
            else:
                print("Invalid choice!")
    def login(self):
        self.id=input("Enter Id:")
        passw=input("Enter Password:")
        with open("patient_credential.txt") as f:
            for i in f.readlines():
                a,b=i.split('|')
                if self.id == a and passw == decode(b.split('\n')[0]):
                    self.run()
    def register(self):
        save_data=[]
        data=("Name","Age","Gender","Contact","Email","Address")
        with open("patient.txt") as fr:
            l=len(fr.readlines())
            save_data.append(f"{l+1:0>5}")
        print('********************************************************')
        for i in data:
            save_data.append(input(f"Enter {i}:"))
        passw=input("Enter Password:")
        print('********************************************************')
        with open("patient.txt","a") as f:
            f.write(f"{'|'.join(save_data)}\n")
        with open("patient_credential.txt","a") as f1:
            passw1=encode(passw)
            f1.write(f"{save_data[0]}|{passw1}\n")
        print(f"Registered your Id is {save_data[0]}")
    def run(self):
        while True:
            print('********************************************************')
            print("""\t\t1.Profile
                2.Appointment
                3.View Doctor's
                4.Exit""")
            print('********************************************************')
            choice = input("Enter choice:")
            options={'1':self.profile,'2':self.appointment,'3':self.view}
            if choice == '4':
                break
            elif int(choice) > 4:
                print('Invalid choice')
            options[choice]()
    def profile(self):
        with open('patient.txt') as pf:
            for i in pf.readlines():
                if self.id == i.split('|')[0]:
                    v=i.split('|')
                    print(f'Patient Id:{v[0]}\nPatient Name:{v[1]}\nPatient Age:{v[2]}')
                    print(f"Patient Gender:{v[3]}\nPatient Contact:{v[4]}\nPatient Email:{v[5]}\nPatient Address:{v[6]}")
    def appointment(self):
        while True:
            print('********************************************************')
            print("""\t\t1.Take Appointment
                2.View Appointment History
                3.Exit""")
            print('********************************************************')
            choice = input("Enter choice:")
            if choice == '1':        
                dId=input("Enter Doctor Id:")
                date=input("Enter Appointment Date:")
                problem=input("Enter Problem:")
                print('********************************************************')
                with open("appointment.txt",'a') as af:
                    af.write(f"{self.id}|{dId}|{date}|{problem}\n")
                with open('appointment_history.txt','a') as af1:
                    af1.write(f"{self.id}|{dId}|{date}|{problem}\n")
                print('Appointment Added Successfully')
            elif choice == '2':
                count=0
                with open("appointment_history.txt") as af2:
                    a=af2.readlines()
                    for i in a:
                        if self.id == i.split('|')[0]:
                            print(i)
                            count+=1
                if count == 0:
                    print("No Record")
                else:
                    print(f'Total Record:{count}')
            elif choice == '3':
                break
            else:
                print('Invalid choice')
    def view(self):
        with open("doctor.txt") as df:
            print(df.read().center(10))
def encode(pas):
    try:
        p1=pas.encode('ascii')
        p2=base64.b64encode(p1)
        p3=p2.decode('ascii')
        return p3
    except:
        print('Error while Encode')
def decode(pas):
    try:
        p1=pas.encode('ascii')
        p2=base64.b64decode(p1)
        p3=p2.decode('ascii')
        return p3
    except:
        print('Error while decode')
if __name__=='__main__':
    while True:
        print('************** Hospital Management System **************')
        print('''\t\t1.Admin login
                2.Doctor login
                3.Patient login
                4.Exit''')
        print('********************************************************')
        choice = input("Enter Choice:")
        if choice == "1":
            if input("Enter username:") =="admin" and input("Enter password:") == "admin":
                admin()
            else:
                print("invalid")
        elif choice == "2":
            doctor()
        elif choice == "3":
            patient()
        elif choice == "4":
            break
        else:
            print('Enter valid choice!')