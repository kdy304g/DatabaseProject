######################################################################
#
# HOMEWORK 3
#
# Due: Sun 3/17/19 23h59.
#
# Name: Danny Kang, Seungin Lyu
#
# Email: dong.kang@students.olin.edu, seungin.lyu@students.olin.edu
#
# Remarks, if any:
#
#
######################################################################


######################################################################
#
# Python 3 code
#
# Please fill in this file with your solutions and submit it
#
# The functions below are stubs that you should replace with your
# own implementation.
#
######################################################################
import pyparsing as pp


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


BOOKS = Relation(["title", "year", "numberPages", "isbn"],
                 ["isbn"],
                 [
    ("A Distant Mirror", 1972, 677, "0345349571"),
    ("The Guns of August", 1962, 511, "034538623X"),
    ("Norse Mythology", 2017, 299, "0393356182"),
    ("American Gods", 2003, 591, "0060558121"),
    ("The Ocean at the End of the Lane", 2013, 181, "0062255655"),
    ("Good Omens", 1990, 432, "0060853980"),
    ("The American Civil War", 2009, 396, "0307274939"),
    ("The First World War", 1999, 500, "0712666451"),
    ("The Kidnapping of Edgardo Mortara", 1997, 350, "0679768173"),
    ("The Fortress of Solitude", 2003, 509, "0375724886"),
    ("The Wall of the Sky, The Wall of the Eye",
     1996, 232, "0571205992"),
    ("Stories of Your Life and Others", 2002, 281, "1101972120"),
    ("The War That Ended Peace", 2014, 739, "0812980660"),
    ("Sheaves in Geometry and Logic", 1994, 630, "0387977102"),
    ("Categories for the Working Mathematician",
     1978, 317, "0387984032"),
    ("The Poisonwood Bible", 1998, 560, "0060175400")
])


PERSONS = Relation(["firstName", "lastName", "birthYear"],
                   ["lastName"],
                   [
                       ("Barbara", "Tuchman", 1912),
                       ("Neil", "Gaiman", 1960),
                       ("Terry", "Pratchett", 1948),
                       ("John", "Keegan", 1934),
                       ("Jonathan", "Lethem", 1964),
                       ("Margaret", "MacMillan", 1943),
                       ("David", "Kertzer", 1948),
                       ("Ted", "Chiang", 1967),
                       ("Saunders", "Mac Lane", 1909),
                       ("Ieke", "Moerdijk", 1958),
                       ("Barbara", "Kingsolver", 1955)
])


AUTHORED_BY = Relation(["isbn", "lastName"],
                       ["isbn", "lastName"],
                       [
                           ("0345349571", "Tuchman"),
                           ("034538623X", "Tuchman"),
                           ("0393356182", "Gaiman"),
                           ("0060558121", "Gaiman"),
                           ("0062255655", "Gaiman"),
                           ("0060853980", "Gaiman"),
                           ("0060853980", "Pratchett"),
                           ("0307274939", "Keegan"),
                           ("0712666451", "Keegan"),
                           ("1101972120", "Chiang"),
                           ("0679768173", "Kertzer"),
                           ("0812980660", "MacMillan"),
                           ("0571205992", "Lethem"),
                           ("0375724886", "Lethem"),
                           ("0387977102", "Mac Lane"),
                           ("0387977102", "Moerdijk"),
                           ("0387984032", "Mac Lane"),
                           ("0060175400", "Kingsolver")
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
    "Books": BOOKS,
    "Persons": PERSONS,
    "AuthoredBy": AUTHORED_BY
}


def convert_abstract_query(db, aq):
    q = {
        "select": aq["select"],
        "from": [(db[name], nickname) for name, nickname in aq["from"]],
        "where": aq["where"]
    }
    return q


# Repeatedly read a line of input, parse it, and evaluate the result
def shell(db):
    print("Available tables:")
    [print("  " + k) for k in db.keys()]
    while(1):
        # receive input and process query
        s = input()
        c = s.find(':')
        # if colon identifier exists
        if(c > -1):
            create = True
            rName = s.split(':')[0]
            s = s[c+1::]
        else:
            create = False

        aq = parseQuery(s)
        q = convert_abstract_query(db, aq)
        r = evaluate_query(q)
        print(r)
        if(create):
            print("Relation "+rName+ " created")
            db[rName] = r

shell(sample_db)
