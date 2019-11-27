import sys
from typing import List
import pygame
import traceback
from PIL import Image
from io import BytesIO
import Logger


NEGATION = "¬"
AND = "∧"
OR = "∨"
EQUAL = "⇔"
IMPLIES = "⇒"

LINKS = [AND, OR, EQUAL, IMPLIES]

LineThickness = 1
Font = "PLFTG\AsanaMath.otf"
BkColor = (255, 255, 255)
HeadColor = (150, 150, 150)
FontColor = (0, 0, 0)
FontSize = 16
LineColor = (0, 0, 0)


class NoFormulaError(Exception):

    def __init__(self, msg):
        self.message = msg

def makePic(form: str):
    pygame.init()
    con = form
    con = con.replace("!", NEGATION).replace("&", AND).replace("|", OR)
    con = con.replace("<->", EQUAL).replace("->", IMPLIES)
    Form = LogicFormula(con)
    table = Form.getTabel()
    FONT = pygame.font.Font("PLFTG\AsanaMath.otf", FontSize)
    tablePic = []
    for row in table:
        Row = []
        for S in row:
            text = FONT.render(S, True, FontColor)
            Row.append(text)
        tablePic.append(Row)
    colume_widths = []
    for i in range(0, len(tablePic[0])):
        width = 0
        for row in tablePic:
            if row[i].get_width() > width:
                width = row[i].get_width()
        colume_widths.append(width+(LineThickness*5))
    width = (len(tablePic[0])*LineThickness)+LineThickness
    for w in colume_widths:
        width = width + w
    line_height = tablePic[0][0].get_height()+LineThickness
    height = (len(tablePic)*(LineThickness + line_height))+LineThickness
    Screen = pygame.Surface((width, height))
    Screen.fill(BkColor)
    pygame.draw.rect(Screen, HeadColor, (0, 0, width, LineThickness+line_height))
    for row in tablePic:
        line = tablePic.index(row)
        for E in row:
            colume = row.index(E)
            pre_width = LineThickness*(colume+1)
            for i in range(0, colume):
                pre_width = pre_width + colume_widths[i]
            pre_height = LineThickness*(line+1)+(line*line_height)
            Screen.blit(E, (pre_width+((colume_widths[colume]-E.get_width())/2), pre_height+(LineThickness/2)))
    for i in range(0, len(tablePic[0])+1):
        x = i*LineThickness
        for I in range(0, i):
            x = x + colume_widths[I]
        pygame.draw.rect(Screen, LineColor, (x, 0, LineThickness, height))
    for i in range(0, len(tablePic)+1):
        y = i*LineThickness
        for I in range(0, i):
            y = y+line_height
        pygame.draw.rect(Screen, LineColor, (0, y, width, LineThickness))
    return Screen


def showTable(form: str):
    pygame.init()
    Surface = makePic(form)
    Screen = pygame.display.set_mode(Surface.get_size())
    Screen.blit(Surface, (0, 0))
    pygame.display.set_caption("LogicTable generator: "+form)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return Surface
    return Surface


def save(pic, file):
    pygame.init()
    pil_string_image = pygame.image.tostring(pic,"RGB",False)
    img = Image.frombytes("RGB",pic.get_size(),pil_string_image)
    buffer = BytesIO()
    img.save(buffer, format = "jpeg")
    open("Tables/" + file, "wb").write(buffer.getvalue())
    

def isFormula(formula: str) -> bool:
    count = 0
    i = 0
    split = list(formula)
    while i < len(split):
        C = split[i]
        if C == NEGATION:
            if len(split) < i + 2:
                print(1)
                return False
            elif split[i + 1] == ")" or LINKS.__contains__(split[i + 1]) or split[i + 1] == NEGATION:
                print(2)
                return False
        elif C == "(":
            count = count + 1
            if len(split) < i + 2:
                print((3))
                return False
            elif split[i + 1] == ")" or LINKS.__contains__(split[i + 1]):
                print(4)
                return False
        elif C == ")":
            count = count - 1
            if count < 0:
                print(5)
                return False
            elif len(split) < i + 1:
                if (not LINKS.__contains__(split[i + 1])) or (not split[i+1] == ")"):
                    print(6)
                    return False
        elif LINKS.__contains__(C):
            if i < 1 or len(split) <= i + 1:
                print(7)
                return False
            elif LINKS.__contains__(split[i + 1]) or split[i + 1] == ")":
                print(8)
                return False
        else:
            if len(split) > i + 1 and split[i + 1] == "(":
                print(9)
                return False
            elif i > 0 and len(split) > i + 1 and LINKS.__contains__(split[i - 1]) and LINKS.__contains__(split[i + 1]):
                print(10)
                return False
        i = i + 1
    return True


class BaseExpression(object):
    name: str

    def __init__(self, name: str):
        self.name = name

    def getState(self) -> bool:
        return False

    def getSubExpressions(self):
        return list()

    def getForm(self) -> str:
        return self.name

    def getCount(self) -> int:
        return 1


class Variable(BaseExpression):
    state: bool

    def __init__(self, name: str):
        super().__init__(name)
        self.state = False

    def setState(self, bool):
        self.state = bool

    def getState(self) -> bool:
        return self.state


class NegativExpression(BaseExpression):
    expr: BaseExpression

    def __init__(self, name: str, expr):
        super().__init__(name)
        self.expr = expr

    def getState(self) -> bool:
        return not self.expr.getState()

    def getSubExpressions(self):
        out = []
        prev = self.expr.getSubExpressions()
        if prev is not None:
            for E in prev:
                out.append(E)
        out.append(self)
        return prev

    def getCount(self) -> int:
        return self.expr.getCount()+1


class LinkedExpression(BaseExpression):
    expr1: BaseExpression
    expr2: BaseExpression
    link: str

    def __init__(self, name: str, expr1: BaseExpression, link: str, expr2: BaseExpression):
        super().__init__(name)
        self.expr1 = expr1
        self.expr2 = expr2
        if not LINKS.__contains__(link):
            raise Exception
        self.link = link

    def getState(self) -> bool:
        if self.link == AND:
            return self.expr1.getState() and self.expr2.getState()
        elif self.link == OR:
            return self.expr1.getState() or self.expr2.getState()
        elif self.link == EQUAL:
            return self.expr1.getState() == self.expr2.getState()
        elif self.link == IMPLIES:
            if self.expr1.getState():
                return self.expr2.getState()
            else:
                return True

    def getSubExpressions(self):
        out = []
        prev1 = self.expr1.getSubExpressions()
        prev2 = self.expr2.getSubExpressions()
        if prev1 is not None:
            for E in prev1:
                out.append(E)
        if prev2 is not None:
            for E in prev2:
                out.append(E)
        out.append(self)
        print(self.name, "len:", len(out), "should:", self.getCount(), "lost:", abs(len(out)-self.getCount()))
        return out

    def getCount(self) -> int:
        return self.expr1.getCount()+self.expr2.getCount()+1


class LogicFormula(object):
    expression: BaseExpression
    expressions: List[BaseExpression]
    formula: str

    def __init__(self, formula: str):
        otherChars = []
        exceptedChars = [NEGATION, AND, OR, EQUAL, IMPLIES, "(", ")"]
        form = formula.replace(" ", "").upper()
        self.log = Logger.Log()
        split = list(form)
        for C in split:
                if not exceptedChars.__contains__(C):
                        c = C
                        C = C.upper()
                        if not c.isalpha():
                                form.replace(c, "")
                        else:
                                if not otherChars.__contains__(C):
                                        otherChars.append(C)
                                        form.replace(c, C)
        if not isFormula(form):
            raise NoFormulaError(form + " >>> wrong Syntax!")
        self.formula = form
        self.expressions = list()
        self.variables = {}
        self.vars = []
        for C in otherChars:
            var = Variable(C)
            self.variables[C] = var
            self.vars.append(var)
        self.expression = self.getExpression(form)
        self.log.close()
        if len(self.expressions) > 0:
            self.expressions[-1] = self.expression
        else:
            self.expressions = [self.expression]

    def getTabel(self) -> List[List[str]]:
        out = []
        v_keys = list(self.variables.keys())
        exprs = self.expressions
        for i in range(0, 2 ** len(self.variables)+1):
            out.append(list())

        # --===<  Bubbel Sort  >===--
        for i1 in range(1, len(v_keys)+1):
            for i2 in range(i1, len(v_keys)):
                if v_keys[i2-1] > v_keys[i2]:
                    temp = v_keys[i2-1]
                    v_keys[i2-1] = v_keys[i2]
                    v_keys[i2] = temp

        def boolToStr(bool: bool) -> str:
            if bool:
                return "1"
            else:
                return "0"

        # Header
        for V in v_keys:
            out[0].append(V)
        for E in exprs:
            out[0].append(E.getForm())

        # Body
        for L in out[1:]:
            trueLine = out.index(L)
            line = trueLine-1
            for V in v_keys:  # setState correct State for all Variables
                rev_index = len(v_keys)-(v_keys.index(V)+1)
                step_size = 2 ** rev_index
                step = (line + (step_size - (line % step_size))) / step_size
                var = self.variables.get(V)
                var.setState(step % 2 == 0)
                out[trueLine].append(boolToStr(var.getState()))
            for E in exprs:
                out[trueLine].append(boolToStr(E.getState()))

        return out

    def makeTabel(self):
        name = self.formula + ".txt"
        file = open(name, 'w', encoding="utf-8")
        table = self.getTabel()

        for row in table:
            line = ""
            for e in row:
                line = line + e + "|"
            line = line[:-1] + "\n"
            file.write(line)

        file.close()
        print("made LogicTable:", name)

    def getExpression(self, formula: str) -> BaseExpression:
        #print("get Expression for:", formula)
        self.log.print(formula)
        if self.variables.__contains__(formula):
            return self.variables.get(formula)
        i = 0
        neg = None
        split = list(formula)
        if formula.startswith(NEGATION):
            if split[1] == "(":
                count = 1
                out = "("
                i = 2
                while count > 0 and i < len(split):
                    C = split[i]
                    if C == "(":
                        count = count + 1
                        out = out + C
                    elif C == ")":
                        count = count - 1
                        out = out + C
                    else:
                        out = out + C
                    i = i + 1
                neg = NegativExpression(NEGATION + out, self.getExpression(out))
            else:
                neg = NegativExpression(NEGATION + split[1], self.getExpression(split[1]))
                i = 2
        if neg is not None:
            #self.expressions.append(neg)
            if i < len(split)-1:
                link = split[i]
                b = ""
                count = 0
                i = i + 1
                while i < len(split):
                    C = split[i]
                    if C == "(":
                        count = count + 1
                        b = b + C
                    elif C == ")":
                        count = count - 1
                        b = b + C
                    else:
                        b = b + C
                    if count == 0 and C != NEGATION:
                        break
                    i = i+1
                expr = LinkedExpression(neg.getForm()+link+b, neg, link, self.getExpression(b))
                self.expressions.append(expr)
                return expr
            else:
                return neg
        count = 0
        a = ""
        link = ""
        lin = 0
        i = 0
        while i < len(split):
            C = split[i]
            if C == "(":
                count = count + 1
                a = a + C
            elif C == ")":
                count = count - 1
                a = a + C
            else:
                if count == 0:
                    if LINKS.__contains__(C):
                        link = C
                        lin = i
                        break
                    else:
                        a = a + C
                else:
                    a = a + C
            i = i + 1
        if link == "":
            if a.startswith("("):
                a = a[1:-1]
            return self.getExpression(a)
        b = ""
        count = 0
        i = lin + 1
        b = formula[i:]
        expr = LinkedExpression(a+link+b, self.getExpression(a), link, self.getExpression(b))
        self.expressions.append(expr)
        return expr
