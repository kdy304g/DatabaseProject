######################################################################
#
# Database Project by Seungin Lyu and Danny Kang
# An Attempt to add roles and security
# Lessone learned : Adding Roles is difficult
# OlinDB
#
######################################################################
import pyparsing as pp
import getpass
<<<<<<< HEAD:CarSalesDB.py

=======
>>>>>>> 602ef2496bcae0026479ce3d2e46aa2d11dd5548:CarSalesDB.py

class Relation:

    def __init__(self, columns, primary_key, tuples=[]):

        self._columns = columns
        self._primary_key = primary_key
        self._tuples = set(tuples)

    def __repr__(self):

        result = "------------------------------------------------------------\n"
        result += (", ".join(self._columns)) + "\n"
        result += "------------------------------------------------------------\n"
        result += "".join([str(t) + "\n" for t in self._tuples])
        result += "------------------------------------------------------------"
        return result

    def columns(self):

        return self._columns

    def primary_key(self):

        return self._primary_key

    def tuples(self):

        return self._tuples

    # helper function that returns a list of indexes corresponding to primary keys
    def p_indexes(self):
        return [self.columns().index(p_key) for p_key in self._primary_key]

    ########################################
    # LOW-LEVEL CRUD OPERATIONS
    ########################################

    def create_tuple(self, tup):
        # check column length
        if (len(tup) != len(self.columns())):
            raise Exception('ValueError: Incorrect number of attributes!')
        # check given p_key already exists
        for tuple in list(self.tuples()):
            for p_index in self.p_indexes():
                if tuple[p_index] == tup[p_index]:
                    raise Exception(
                        'KeyError:tuple with given primary key already exists!')
        self._tuples.add(tup)

    def read_tuple(self, pkey):
        for tup in self.tuples():
            p_tuple = [tup[p_index] for p_index in self.p_indexes()]
            if pkey == tuple(p_tuple):
                return tup
        raise Exception('KeyError: no tuple with given primary key found')

    def delete_tuple(self, pkey):
        tuples = self.tuples().copy()
        for tup in tuples:
            p_tuple = [tup[p_index] for p_index in self.p_indexes()]
            if pkey == tuple(p_tuple):
                return self.tuples().remove(tup)
        raise Exception('KeyError: no tuple with given primary key found')

    ########################################
    # RELATIONAL ALGEBRA OPERATIONS
    ########################################

    def project(self, names):
        # check if names is a subset of columns
        for name in names:
            if name not in self.columns():
                raise Exception('KeyError: No ' + name + ' column found')
        project_primary_key = [
            self._primary_key for p_key in self._primary_key if p_key in names]
        attr_indexes = [self.columns().index(name) for name in names]
        project_tuples = []
        for elem in self.tuples():
            project_tuple_lst = [elem[index] for index in attr_indexes]
            project_tuples.append(tuple(project_tuple_lst))
        return Relation(names, project_primary_key, project_tuples)

    def select(self, pred):
        select_tuples = []
        for tuple in self._tuples:
            tuple_dic = {}
            attr_index = 0
            for value in tuple:
                tuple_dic[self._columns[attr_index]] = value
                attr_index += 1
            if pred(tuple_dic):
                select_tuples.append(tuple)
        return Relation(self._columns, self._primary_key, select_tuples)

    def union(self, rel):
        if rel.columns() != self.columns():
            raise Exception(
                "Schema of the new relation must be the same")
        if rel.primary_key() != self.primary_key():
            raise Exception(
                "Schema of the new relation must be the same")
        union_tuples = list(self.tuples().union(rel.tuples()))
        return Relation(self._columns, self._primary_key, union_tuples)

    def rename(self, rlist):
        rename_columns = []
        rename_p_key = []
        oldNames = [pair[0] for pair in rlist]
        newNames = [pair[1] for pair in rlist]
        for p_key in self.primary_key():
            if p_key in oldNames:
                rename_p_key.append(newNames[oldNames.index(p_key)])
            else:
                rename_p_key.append(p_key)
        for attribute in self.columns():
            if attribute in oldNames:
                rename_columns.append(newNames[oldNames.index(attribute)])
            else:
                rename_columns.append(attribute)
        return Relation(rename_columns, rename_p_key, self.tuples())

    def product(self, rel):
        product_coloumns = []
        product_p_key = []
        product_tuples = []

        for attribute in self._columns:
            if attribute in rel._columns:
                raise Exception("some attributes overlap between relations..")
        product_columns = self._columns + rel._columns
        product_p_key = self._primary_key + rel._primary_key

        for s_tuple in self._tuples:
            for rel_tuple in rel._tuples:
                product_tuples.append((s_tuple + rel_tuple))

        return Relation(product_columns, product_p_key, product_tuples)

    def aggregate(self, aggr):
        res = []
        for (name, op, attr) in aggr:
            project = self.project([attr]).tuples()
            if op == 'sum':
                val = tuple(sum(x) for x in zip(*project))[0]
            if op == 'count':
                val = len(project)
            if op == 'avg':
                val = (tuple(sum(x)
                             for x in zip(*project))[0]) / (len(project))
            if op == 'max':
                val = max(project)[0]
            if op == 'min':
                val = min(project)[0]
            res.append(val)
        return Relation([name for (name, _, _) in aggr], [], [tuple(res)])

    def aggregateByGroup(self, aggr, groupBy):

        pass


CARS = Relation(["cid", "name", "type", "color", "price", "number_sold"],
                 ["cid"],
                 [
                    (1, "Ford Explorer", "suv", "blue", 36675, 0),
                    (2, "Ford Escape", "suv", "white", 24105, 0),
                    (3, "Volkswagen Tiger", "suv", "red", 24295, 0),
                    (4, "Jeep Grand Cherokee", "suv", "red", 31945, 0),
                    (5, "Honda CR-V", "suv", "silver", 24350, 0),
                    (6, "Toyota RAV4", "suv", "space grey", 25500, 0),
                    (7, "Toyota Highlander", "suv", "sky blue", 31530, 0),
                    (8, "Kia Sorento", "suv", "black", 26290, 0),
                    (9, "Ford Expedition", "suv", "black", 52130, 0),
                    (10, "Chevrolet Equinox", "suv", "white", 24295, 0),
                    (11, "Toyota Camry", "sedan", "white", 23945, 0),
                    (12, "Ford Fusion", "sedan", "white", 22840, 0),
                    (13, "Nissan Altima", "sedan", "white", 23900, 0),
                    (14, "Honda Accord", "sedan", "black", 23720, 0),
                    (15, "Toyota Camry", "sedan", "white", 23945, 0),
                    (16, "Hyundai Sonata", "sedan", "blue", 22500, 0),
                    (17, "Hyundai Elantra", "sedan", "white", 17200, 0),
                    (18, "Subaru Legacy", "sedan", "white", 22545, 0),
                    (19, "Audi A4", "sedan", "grey", "37400", 0),
                    (20, "Toyota Corolla", "sedan", "black", 19500, 0),
                    (21, "Ford Mustang", "coupe", "green", 26395, 0),
                    (22, "Dodge Challenger", "coupe", "grey", 27845, 0),
                    (23, "Chevrolet Camaro", "coupe", "gold", 25000, 0),
                    (24, "Honda Civic", "coupe", "blue", 19450, 0),
                    (25, "Porsche 911", "coupe", "white", 113300,0),
                    (26, "Lexus RC", "coupe", "black", 64750,0),
                    (27, "Audi S5", "coupe", "white", 52400,0),
                    (28, "Toyota 86", "coupe", "black", 26505,0),
                    (29, "BMW 4series", "coupe", "blue", 44750,0),
                    (30, "Infiniti Q60", "coupe", "grey", 40750,0)

])

USERS = Relation(["id", "password", "name", "role"],
                   ["id"],
                   [
                        ("kdy304g", "1234", "Danny", "Manager"),
                        ("slyu", "1234", "Seungin", "Manager"),
                        ("john1", "1234", "John", "Employee"),
                        ("doe1", "1234", "Doe", "Customer")
])

def evaluate_query(query):

    # perform product for each relation in [from] list
    products = None
    for (relation, nickname) in query["from"]:
        r_list = [(attr, nickname + "." + attr) for attr in relation.columns()]
        renamed = relation.rename(r_list)
        if(products is not None):
            products = products.product(renamed)
        else:
            products = renamed
    # perform select for each predicate
    select = products
    for (op, arg1, arg2) in query["where"]:
        if op == "n=n":
            p = (lambda t: t[arg1] == t[arg2])
        elif op == "n=v":
            p = (lambda t: t[arg1] == arg2)
        elif op == "n>v":
            p = (lambda t: t[arg1] > arg2)
        select = select.select(p)
    # perform projection for each select attr
    project = select.project(query["select"])

    return project


def evaluate_query_aggr(query):
    attributes = list(set([attr for (_, _, attr) in query["select-aggr"]]))
    query1 = {
        "select": attributes,
        "from": query["from"],
        "where": query["where"]
    }
    return evaluate_query(query1).aggregate(query["select-aggr"])


def evaluate_query_aggr_group(query):

    pass


def parseQuery(input):

    # parse a string into an abstract query

    # <sql> ::= select <columns> from <tables> (where <conditions>)?

    idChars = pp.alphas + "_*"

    pIDENTIFIER = pp.Word(idChars, idChars + "0123456789.")
    pIDENTIFIER.setParseAction(lambda result: result[0])

    pCOMMAIDENT = pp.Suppress(pp.Word(",")) + pIDENTIFIER

    pIDENTIFIER2 = pp.Group(pIDENTIFIER + pIDENTIFIER)

    pCOMMAIDENT2 = pp.Suppress(pp.Word(",")) + pIDENTIFIER2

    pINTEGER = pp.Word("-0123456789", "0123456789")
    pINTEGER.setParseAction(lambda result: int(result[0]))

    pSTRING = pp.QuotedString("'")

    def pKEYWORD(w): return pp.Suppress(pp.Keyword(w,caseless=True))

    pSELECT = pKEYWORD("select") + pp.Group(pIDENTIFIER +
                                            pp.ZeroOrMore(pCOMMAIDENT))

    pFROM = pKEYWORD("from") + pp.Group(pIDENTIFIER2 +
                                        pp.ZeroOrMore(pCOMMAIDENT2))

    pCONDITION_NEQN = pIDENTIFIER + pp.Word("=") + pIDENTIFIER
    pCONDITION_NEQN.setParseAction(
        lambda result: ("n=n", result[0], result[2]))

    pCONDITION_NEQV1 = pIDENTIFIER + pp.Word("=") + pINTEGER
    pCONDITION_NEQV1.setParseAction(
        lambda result: ("n=v", result[0], result[2]))

    pCONDITION_NEQV2 = pIDENTIFIER + pp.Word("=") + pSTRING
    pCONDITION_NEQV2.setParseAction(
        lambda result: ("n=v", result[0], result[2]))

    pCONDITION_NGEV = pIDENTIFIER + pp.Word(">") + pINTEGER
    pCONDITION_NGEV.setParseAction(
        lambda result: ("n>v", result[0], result[2]))

    pCONDITION = pCONDITION_NEQV1 | pCONDITION_NEQV2 | pCONDITION_NEQN | pCONDITION_NGEV

    pANDCONDITION = pKEYWORD("and") + pCONDITION

    pCONDITIONS = pp.Group(pCONDITION + pp.ZeroOrMore(pANDCONDITION))

    pWHERE = pp.Optional(pKEYWORD("where") + pCONDITIONS)

    pSQL = pSELECT + pFROM + pWHERE + pp.StringEnd()
    pSQL.setParseAction(lambda result: {"select": result[0].asList(),
                                        "from": result[1].asList(),
                                        "where": result[2].asList() if len(result) > 2 else []})

    result = pSQL.parseString(input)[0]
    return result    # the first element of the result is the expression


sample_db = {
    "Cars": CARS,
    "Users": USERS
}


def convert_abstract_query(db, aq):
    q = {
        "select": aq["select"],
        "from": [(db[name], nickname) for name, nickname in aq["from"]],
        "where": aq["where"]
    }
    return q

Role_Table = {
    "Manager": ["Create", "Read", "Update", "Delete"],
    "Employee": ["Read", "Update"],
    "Customer": ["Read"]
}

# Repeatedly read a line of input, parse it, and evaluate the result
def shell(db):

    while(True):
        print("-----------------Weclome to Danny&Seungin Car Sales------------------")
        print()
        print("1. Login \n2. Create New Account")
        print()
        print("----------------------------------------------------------------")
        print()
        option = input("Choose from menu: ")
        userRole = None
        loginStatus = False
        # Log in
        if option == "1":
            while(userRole == None):
                userID = input("Enter your ID: ")
                try:
                    userInfo = USERS.read_tuple((userID,))
                    userRole = userInfo[3]
                    while not loginStatus:
                        password = getpass.getpass('Password:')
                        if userInfo[1] == password:
                            print("Log in success!")
                            loginStatus = True
                        else:
                            print("Wrong password!")
                except:
                    print("User with given userID does not exist")
<<<<<<< HEAD:CarSalesDB.py
    # Create new account
=======
        # Create new account
>>>>>>> 602ef2496bcae0026479ce3d2e46aa2d11dd5548:CarSalesDB.py
        elif option == "2":
            while(True):
                userRole = input("Enter your role: 1 -> Manager, 2-> Employee, 3-> Customer\n")
                # this prevents users from entering the wrong role type
                if userRole == '1':
                    userRole = 'Manager'
                    break
                elif userRole == '2':
                    userRole = 'Employee'
                    break
                elif userRole == '3':
                    userRole = 'Customer'
                    break
                print("Invalid Role, please choose from option 1,2,3")

            userName = input("Enter your name: ")
            while not loginStatus:
                userID = input("Enter your ID: ")
                try:
                    USERS.read_tuple((userID,))
                    print("That ID already exists! Please try again.")
                except:
                    loginStatus = True
            password = getpass.getpass('Enter you Password:')
<<<<<<< HEAD:CarSalesDB.py
            userInfo = (userName, userID, password, userRole, 0, 0)
            # print(userInfo)
            USERS.create_tuple(userInfo)
            # print(USERS)
        print()
        print("Log in success!")
        print()
=======
            userInfo = (userID, password, userName, userRole)
            print("logged in as", userID)
            USERS.create_tuple(userInfo)


        # after creating an account and logged in
>>>>>>> 602ef2496bcae0026479ce3d2e46aa2d11dd5548:CarSalesDB.py

        if userRole == 'Manager':
            while(True):
                print("----------------------------Menu----------------------------\n")
                print("1.Create")
                print("2.Read")
                print("3.Update")
                print("4.Delete")
                print("5.Quit")
                print("------------------------------------------------------------\n")
                option = input("Choose from menu: ")
                if option == "1":
                    print("Available tables:")
                    print([k for k in db.keys()])
                    table = input("Choose table to operate CRUD operations: ")
                    data = sample_db[table]
                    print(data)
                    if data == CARS:
                        carName = input("Enter name of the car: ")
                        carType = input("Enter type of the car: ")
                        carColor = input("Enter color of the car: ")
                        carPrice = input("Enter price of the car: ")
                        print("new car created in relation Cars!")
                        cid = len(CARS.tuples())+1
                        CARS.create_tuple((cid, carName, carType, carColor, carPrice, 0))

                    elif data == USERS:
                        # ["name", "id", "password", "role", "number of cars sold", "sales"]
                        userName = input("Enter name of the user: ")
                        userID = input("Enter ID of user: ")
                        userPassword = input("Enter password of user: ")
                        userRole = input("Enter role of the user: ")
                        print("new user created in relations Persons!")
                        uid = len(USERS.tuples())+1
                        USERS.create_tuple((userID, userName, userPassword, userRole))

                elif option == "2":
                    # todo: accept any query
                    try:
<<<<<<< HEAD:CarSalesDB.py
                        print(data.read_tuple((pkey,)))
                        print()
                    except:
                        print("Wrong key!\n")
=======
                        s = input("Input Select Query : \n")
                        aq = parseQuery(s)
                        q = convert_abstract_query(db, aq)
                        r = evaluate_query(q)
                        print(r)
                    except Exception:
                        print("Invalid Query")

>>>>>>> 602ef2496bcae0026479ce3d2e46aa2d11dd5548:CarSalesDB.py
                elif option == "3":
                    print("Available tables:")
                    print([k for k in db.keys()])
                    table = input("Choose table to operate CRUD operations: ")
                    data = sample_db[table]
                    print(data)
                    pkey = input("Enter primary key of data that you want to update: ")
                    try:
                        data.delete_tuple((pkey,))
                        if data == CARS:
                            carName = input("Enter name of the car: ")
                            carType = input("Enter type of the car: ")
                            carColor = input("Enter color of the car: ")
                            carPrice = input("Enter price of the car: ")
                            print("%s updated!" %pkey)
                            CARS.create_tuple((pkey, carName, carType, carColor, carPrice, 0))

                        elif data == USERS:
                            # ["name", "id", "password", "role", "number of cars sold", "sales"]
                            userName = input("Enter name of the user: ")
                            userID = input("Enter ID of user: ")
                            userPassword = input("Enter password of user: ")
                            userRole = input("Enter role of the user: ")
                            print("%s updated!" %pkey)
                            USERS.create_tuple((pkey, userName, userID, userPassword, userRole, 0, 0))

                    except:
                        print("Wrong key! Please try again\n")
                elif option == "4":
                    pkey = input("Enter primary key of data that you want to delete: ")
                    try:
                        data.delete_tuple((pkey,))
                        print("%s is now deleted!" %pkey)
                    except:
                        print("Wrong key!\n")
                elif option == "5":
                    break
        elif userRole == 'Employee':
            while(True):
                print("1.Read")
                print("2.Update")
# <<<<<<< HEAD:OlinDB.py
                print("3.Quit")
                print()
                print("-------------------------------------------------------------------")
                print()
# =======
                # print("3.Quit\n")
                # print("------------------------------------------------------------\n")
# >>>>>>> 4f6b37731319634e05224fdb7a143f2d49f73070:CarSalesDB.py
                option = input("Choose from menu: ")
                if option == "1":
                    try:
<<<<<<< HEAD:CarSalesDB.py
                        print(data.read_tuple((pkey,)))
                        print()
                    except:
                        print("Wrong key!\n")
=======
                        s = input("Input Select Query : \n")
                        aq = parseQuery(s)
                        q = convert_abstract_query(db, aq)
                        r = evaluate_query(q)
                        print(r)
                    except Exception:
                        print("Invalid Query")
>>>>>>> 602ef2496bcae0026479ce3d2e46aa2d11dd5548:CarSalesDB.py
                elif option == "2":
                    pkey = input("Enter primary key of data that you want to update: ")
                    try:
                        data.delete_tuple((pkey,))
                        if data == CARS:
                            carName = input("Enter name of the car: ")
                            carType = input("Enter type of the car: ")
                            carColor = input("Enter color of the car: ")
                            carPrice = input("Enter price of the car: ")
                            print("%s updated!" %pkey)
                            CARS.create_tuple((carName, carType, carColor, carPrice, 0))

                        elif data == USERS:
                            # ["name", "id", "password", "role", "number of cars sold", "sales"]
                            userName = input("Enter name of the user: ")
                            userID = input("Enter ID of user: ")
                            userPassword = input("Enter password of user: ")
                            userRole = input("Enter role of the user: ")
                            print("%s updated!" %pkey)
                            USERS.create_tuple((userID, userName, userPassword, userRole))

                    except:
                        print("Wrong key! Please try again\n")
                elif option == "3":
                    break
        elif userRole == 'Customer':
            while(True):
                print("1.Read")
                print("2.Quit")
                print()
                print("-------------------------------------------------------------------")
                print()
                option = input("Choose from menu: ")
                if option == "1":
                    try:
                        s = input("Input Select Query : \n")
                        if(s.find("Users") != -1):
                            print()
                            print("Access Denied!!\n")
                            print("Access Denied")
                        else:
                            aq = parseQuery(s)
                            q = convert_abstract_query(db, aq)
                            r = evaluate_query(q)
                            print(r)
                    except Exception:
                        print("Invalid Query")
                elif option == "2":
                    break

# run shell
shell(sample_db)
