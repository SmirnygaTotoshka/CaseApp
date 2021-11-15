from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from faker import Faker
import datetime
import random
import re
if __name__ == '__main__':

    def generatePassports():
        fake = Faker("ru_RU")
        numbers = [str(random.randint(3000,5000)) + str(random.randint(100000,900000)) for i in range(200)]
        address = [fake.unique.address() for i in range(200)]
        d = {k:v[:-8] for k,v in zip(numbers, address)}
        return d

    def generatePolices():
        numbers = [str(random.randint(10000000,12000000)) + str(random.randint(10000000,90000000)) for i in range(200)]
        org = [random.randint(20,40) for i in range(200)]
        d = {k: v for k, v in zip(numbers, org)}
        return d

    def generateDoctors():
        fake = Faker("ru_RU")
        sirnames = [fake.unique.last_name_male() for i in range(5)]+[fake.unique.last_name_female() for i in range(10)]
        names = [fake.unique.first_name_male() for i in range(5)]+[fake.unique.first_name_female() for i in range(10)]
        secnames = [fake.unique.middle_name_male() for i in range(5)]+[fake.unique.middle_name_female() for i in range(10)]
        sex = [1,1,1,1,1,2,2,2,2,2,2,2,2,2,2]
        birthdays = [fake.unique.date_between_dates(date_start = datetime.date(1950, 1, 1), date_end = datetime.date(1995, 12, 31)) for i in range(15)]
        pos = [random.randint(15,50) for i in range(15)]
        spec = [random.randint(5,30) for i in range(15)]
        dep = [random.randint(1000,1100) for i in range(15)]
        tel = [fake.unique.phone_number()for i in range(15)]
        for i,t in enumerate(tel):
            k = re.sub("\s+|\(|\)|\-","",t)
            k_new = re.sub("^(8|7|\+7)\d{1}","+79",k)
            tel[i] = k_new

        return (sirnames,names,secnames,sex,birthdays,pos,spec,dep,tel)

    def generatePatients():
        fake = Faker("ru_RU")
        sirnames = [fake.last_name_male() for i in range(80)]+ [fake.last_name_female() for i in range(120)]
        names = [fake.first_name_male() for i in range(80)]+ [fake.first_name_female() for i in range(120)]
        secnames = [fake.middle_name_male() for i in range(80)]+ [fake.middle_name_female() for i in range(120)]
        sex = [1 for i in range(80)]+ [2 for i in range(120)]
        birthdays = [fake.unique.date_between_dates(date_start=datetime.date(1950, 1, 1), date_end=datetime.date(2002, 12, 31)) for i in range(200)]
        priv = [159 for i in range(200)]
        empl = [5 for i in range(200)]
        work = [fake.company() for i in range(200)]
        passport = [i for i in range(1,201)]
        snils = [str(random.randint(10000000000,12000000000))for i in range(200)]
        police = [i for i in range(1,201)]
        stat = [random.randint(1,6) for i in range(200)]
        tel = [fake.unique.phone_number() for i in range(200)]
        for i, t in enumerate(tel):
            k = re.sub("\s+|\(|\)|\-", "", t)
            k_new = re.sub("^(8|7|\+7)\d{1}", "+79", k)
            tel[i] = k_new

        return (sirnames,names,secnames,sex,birthdays,priv,empl,work,passport,snils,police,stat,tel)

    def generateCases():
        mkbs = [4286,4279,4272,3550,3599,3961,4351,3331,4278,4621,4661,6203,2067,5411,3068]
        aid = random.randint(1,5)
        p = random.randint(1,4)
        r = random.randint(1,5)
        m = random.choice(mkbs)
        t = random.randint(1,3)
        return  (aid,p,r,m,t)

    def generateVisit():
        fake = Faker("ru_RU")
        doctor = random.randint(1,15)
        d = datetime.datetime.strftime(fake.unique.date_between_dates(date_start=datetime.date(2018, 1, 1), date_end=datetime.date(2018, 12, 31)), "%Y-%m-%d")
        p = random.randint(1,5)
        c = random.choice([10,11,12,13,14,20])
        return (doctor,d,p,c)

    passports = generatePassports()
    polices = generatePolices()

    database = QSqlDatabase.addDatabase("QODBC")
    database.setDatabaseName('Driver={SQL Server};'
                             'Server=SMIRNYGATOTOSHK\SQLEXPRESS;'
                             'Database=ambulatoryCase;'
                             'Trusted_Connection=yes;')
    if database.open():
        print("Success")
        query = QSqlQuery()

        for i in range(1,1606):
            num_services = random.randint(1,10)
            for j in range(1,num_services+1):
                q = "INSERT INTO tbl_Services VALUES (:v,:c,:t)"
                if query.prepare(q):
                    query.bindValue(":v", i)
                    query.bindValue(":c", random.randint(1088,12140))
                    query.bindValue(":t", 1)
                    if not query.exec():
                        print(query.lastError().text() + " " + str(i) + " " + str(j))
                    else:
                        print(str(i))
                        i += 1
                else:
                    print("Not prepared " + query.lastError().text())

        # for i in range(1,795):
        #     num_visit = random.randint(1,3)
        #     for j in range(1,num_visit+1):
        #         doc,d,p,c = generateVisit()
        #         q = "INSERT INTO tbl_Visit VALUES (:doc,:case,CAST(:d as date),:p,:c)"
        #         if query.prepare(q):
        #             query.bindValue(":doc", doc)
        #             query.bindValue(":case", i)
        #             query.bindValue(":d", d)
        #             query.bindValue(":p", p)
        #             query.bindValue(":c", c)
        #             if not query.exec():
        #                 print(query.lastError().text() + " " + str(i) + " " + str(j))
        #                 break
        #             else:
        #                 print(str(i))
        #                 i += 1
        #         else:
        #             print("Not prepared " + query.lastError().text())


        # for i in range(1,201):
        #     num_cases = random.randint(1,3)
        #     for j in range(1,num_cases+1):
        #         a, p, r, m, t = generateCases()
        #         q = "INSERT INTO tbl_Case VALUES (:pat,:a,:p,:r,:m,:t)"
        #         if query.prepare(q):
        #             query.bindValue(":pat", i)
        #             query.bindValue(":a", a)
        #             query.bindValue(":p", p)
        #             query.bindValue(":r", r)
        #             query.bindValue(":m", m)
        #             query.bindValue(":t", t)
        #             if not query.exec():
        #                 print(query.lastError().text() + " " + str(i) + " " + str(j))
        #                 break
        #             else:
        #                 print(str(i))
        #                 i += 1
        #         else:
        #             print("Not prepared " + query.lastError().text())


        # sirnames,names,secnames,sex,birthdays,priv,empl,work,passport,snils,police,stat,tel = generatePatients()
        # q = "INSERT INTO tbl_Patients VALUES (:s,:n,:sec,:se,CAST(:b as date),:p,:em,:w,:pa,:sni,:po,:st,:t)"
        # if query.prepare(q):
        #     i = 1
        #     for s, n, sec, se, b, p, em, w, pa,sni,po,st,t in zip(sirnames,names,secnames,sex,birthdays,priv,empl,work,passport,snils,police,stat,tel):
        #         query.bindValue(":s", s)
        #         query.bindValue(":n", n)
        #         query.bindValue(":sec", sec)
        #         query.bindValue(":se", se)
        #         sd = datetime.datetime.strftime(b, "%Y-%m-%d")
        #         query.bindValue(":b", sd)
        #         query.bindValue(":p", p)
        #         query.bindValue(":em", em)
        #         query.bindValue(":w", w)
        #         query.bindValue(":pa", pa)
        #         query.bindValue(":sni", sni)
        #         query.bindValue(":po", po)
        #         query.bindValue(":st", st)
        #         query.bindValue(":t", t)
        #         if not query.exec():
        #             print(query.lastError().text() + " " + str(s) + " " + str(n))
        #             break
        #         else:
        #             print(str(i))
        #             i += 1
        # else:
        #     print("Not prepared " + query.lastError().text())


        # sirnames, names, secnames, sex, birthdays, pos, spec, dep, tel = generateDoctors()
        # q = "INSERT INTO tbl_Doctors VALUES (:s,:n,:sec,:se,CAST(:b as date),:p,:sp,:d,:t)"
        # if query.prepare(q):
        #     i = 1
        #     for s,n,sec,se,b,p,sp,d,t in zip(sirnames, names, secnames, sex, birthdays, pos, spec, dep, tel):
        #         query.bindValue(":s", s)
        #         query.bindValue(":n", n)
        #         query.bindValue(":sec", sec)
        #         query.bindValue(":se", se)
        #         sd = datetime.datetime.strftime(b,"%Y-%m-%d")
        #         query.bindValue(":b",sd)
        #         query.bindValue(":p", p)
        #         query.bindValue(":sp", sp)
        #         query.bindValue(":d", d)
        #         query.bindValue(":t", t)
        #         if not query.exec():
        #             print(query.lastError().text() + " " + str(s) + " " + str(n))
        #             break
        #         else:
        #             print(str(i))
        #             i += 1
        # else:
        #     print("Not prepared " + query.lastError().text())


        # q = "INSERT INTO tbl_Polices VALUES (:num,:org)"
        # if query.prepare(q):
        #     for k, v in polices.items():
        #         query.bindValue(":num", k)
        #         query.bindValue(":org", v)
        #         if not query.exec():
        #             print(query.lastError().text() + " " + str(k) + " " + str(v))
        #             break
        #         else:
        #             print(str(k) + " " + str(v))
        # else:
        #     print("Not prepared " + query.lastError().text())




        # q = "INSERT INTO tbl_Passports VALUES (:num,:add)"
        # if query.prepare(q):
        #     for k,v in passports.items():
        #         query.bindValue(":num",k)
        #         query.bindValue(":add",v)
        #         if not query.exec():
        #             print(query.lastError().text() + " " + str(k) + " " + str(v))
        #             break
        #         else:
        #             print(str(k) + " " + str(v))
        # else:
        #     print("Not prepared " + query.lastError().text())

