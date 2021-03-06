class BinaryOperator:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.left, self.right)

    def toSympy(self, op):
        return '(%s%s%s)' % (self.left.toSympy(), op, self.right.toSympy())

class Plus(BinaryOperator):
    def toSympy(self):
        return super().toSympy('+')

class Divide(BinaryOperator):
    def toSympy(self):
        return super().toSympy('/')

class Times(BinaryOperator):
    def toSympy(self):
        return super().toSympy('*')

class Minus(BinaryOperator):
    def toSympy(self):
        return super().toSympy('-')

class Pow(BinaryOperator):
    def toSympy(self):
        return super().toSympy('**')

class Arrow(BinaryOperator):
    def toSympy(self):
        return '%s,%s' % (self.left.toSympy(), self.right.toSympy())

class Eq(BinaryOperator):
    def toSympy(self):
        return super().toSympy('-')



class UnaryOperator:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self.val)

class Opp(UnaryOperator):
    def toSympy(self):
        return '('+ '-' + self.val.toSympy() +')'

class Fact(UnaryOperator):
    def toSympy(self):
        return '(' + self.val.toSympy() +'!)'

class Diff:
    def __init__(self, val, nb):
        self.val = val
        self.nb=nb

    def __str__(self):
        return 'Diff('+str(self.val)+','+str(self.nb)+')'

    def toSympy(self):
        return 'diff('+self.val.toSympy()+','+self.val.args[0].toSympy()+','+str(self.nb)+')'

class List:
    def __init__(self, l):
        self.list = l

    def __str__(self):
        if len(self.list)==0:
            return 'List([])'
        s = 'List(['+str(self.list[0])
        for e in self.list[1:]:
            s = s + ', ' + str(e)
        return s+'])'

    def __getitem__(self,index):
        return self.list[index]

    def __add__(self, other):
        return List(self.list+other.list)

    def __len__(self):
        return len(self.list)

    def getList(self):
        return self.list

    def toSympy(self):
        if len(self.list)==0:
            return ''
        s = self.list[0].toSympy()
        for e in self.list[1:]:
            s = s + ', ' + e.toSympy()
        return s

class FunctionCall:
    def __init__(self, function, args):
        self.function = function
        self.args = args

    def __str__(self):
        return 'FunctionCall('+str(self.function)+','+str(self.args)+')'

    def toSympy(self):
        if type(self.function)==Id:
            return self.translate(self.function.toSympy(), self.args)

    def translate(self, function, args):
        mathematicaToSympy={'Sqrt' : (lambda a: 'sqrt('+a[0].toSympy()+')'),
                            'Sin' : (lambda a: 'sin('+a[0].toSympy()+')'),
                            'Cos' : (lambda a: 'cos('+a[0].toSympy()+')'),
                            'Tan' : (lambda a: 'tan('+a[0].toSympy()+')'),
                            'Arccos' : (lambda a: 'acos('+a[0].toSympy()+')'),
                            'Arcsin' : (lambda a: 'asin('+a[0].toSympy()+')'),
                            'Arctan' : (lambda a: 'atan('+a[0].toSympy()+')'),
                            'Sum' : (lambda a: 'summation('+a[0].toSympy()+''.join(([(lambda l:',('+l[0].toSympy()+',('+ l[1].toSympy() +','+ l[2].toSympy() +'))')(l) for l in a[1:]]))+')'),
                            'Integrate' : (lambda a: 'integrate('+a[0].toSympy()+''.join(list(reversed([(lambda l:',('+l.toSympy()+')')(l) for l in a[1:]])))+')'),
                            'N' : (lambda a: 'N('+a.toSympy()+')'),
                            'D' : (lambda a: 'diff('+a[0].toSympy()+', '+', '.join([l.toSympy() for l in a[1:]])+')'),
                            'Exp' : (lambda a: 'exp('+a.toSympy()+')'),
                            'Simplify' : (lambda a: 'simplify('+a.toSympy()+')'),
                            'Power' : (lambda a: 'Pow('+a.toSympy()+')'),
                            'Log' : (lambda a: 'log('+List(list(reversed(a.getList()))).toSympy()+')'),
                            'Log10' : (lambda a: '(log('+a[0].toSympy()+'))/(log(10))'),
                            'Log2' : (lambda a: '(log('+a[0].toSympy()+'))/(log(2))'),
                            'Factorial' : (lambda a: '('+a[0].toSympy()+'!)'),
                            'Abs' : (lambda a: 'Abs('+a[0].toSympy()+')'),
                            'Ceiling' : (lambda a: 'ceiling('+a[0].toSympy()+')'),
                            'Floor' : (lambda a: 'floor('+a[0].toSympy()+')'),
                            'Limit' : (lambda a: 'limit('+a[0].toSympy() +','+ a[1].toSympy()+')'),
                            'Solve' : (lambda a: 'solve(['+a[0].toSympy() +'],['+ a[1].toSympy()+'])'),
                           }

        for name in mathematicaToSympy.keys():
            if name == function:
                return '('+mathematicaToSympy[name](args)+')'

        return '('+function+'('+ self.args.toSympy() +')'+')'

class Id:
    def __init__(self, id):
        self.id=id

    def __str__(self):
        return 'Id('+str(self.id)+')'

    def toSympy(self):
        return self.translateId(self.id)

    def translateId(self, id):
        mathematicaToSympy={'Infinity' : 'oo',
                            'I' : 'I',
                            'Pi' : 'pi',
                            'GoldenRatio' : 'GoldenRatio',
                            'EulerGamma' : 'EulerGamma',
                           }
        if id in mathematicaToSympy.keys():
            return mathematicaToSympy[id]
        return str(id)
