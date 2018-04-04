import ply.yacc as yacc
import sys
from lexer import tokens
import types
import sym_table
body =""
filename = sys.argv[1]

def type(a):
	try:
		float(a)
		try:
			int(a)
			if(int(a)==float(a)):
				return 'int'
			else:
				return 'float'
		except:
			return 'float'
	except:
		return 'string'

relop={
	"<=":'leq',
	"<":'lt',
	">=":'geq',
	">":'gt',
	"==":'eq',
	"!=":'neq'
}
precedence = (
    ('right','EQUAL', 'NOT'),
    ('left', 'LOGICAL_OR'),
    ('left', 'LOGICAL_AND'),
    ('left', 'BINARY_OR'),
    ('left', 'BINARY_XOR'),
    ('left', 'BINARY_AND'),
    ('left', 'EQUAL', 'NOT_EQUALS'),
    ('left', 'LESS_THAN', 'GREATER_THAN','LESS_THAN_EQ','GREATER_THAN_EQ'),
    ('left', 'BINARY_LSHIFT', 'BINARY_RSHIFT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE','REMAINDER'),
)


# def printfinal(tree,counter):
# 	global body
# 	allLeaves = True
# 	if (type(tree) == None):
# 		return tree
# 	else:
# 		for i in range(1,len(tree)):
# 			if(isinstance(tree[i], types.StringTypes) == True):
# 				if "#" in tree[i]:
# 					tree[i] = tree[i][:-1]
# 					body = body + "<b>" + " " + tree[i] + "</b>"
# 				else:
# 					body = body + " " + tree[i]
# 			else:
# 				tree[i] = printfinal(tree[i], (allLeaves and counter))
# 				allLeaves = False
# 		if(allLeaves == True and counter == True):
# 			tree = tree[0]+"#"
# 		return tree

# def printRightDeriv(tree):
# 	global body
# 	while(isinstance(tree, types.StringTypes) == False):
# 		tree = printfinal(tree,True)
# 		print body + "<br>"
# 		body = ""
# 	print "<b>" + tree[:-1] + "</b>" + "<br>"

def printfinal(node):
	print
	print
	print ''.join(node.code)
	print
	print st.table

class Node:
	def __init__(self):
		self.type=""
		self.code=[]
		self.place=""
		self.place2=""
		self.label=""
		# self.next=None

st = sym_table.Symtable()

def p_program(p):
	'''program : compstmt'''
	p[0] = p[1]
	printfinal(p[0])

def p_compstmt(p):
	'''compstmt : stmts opt_terminals'''
	p[0] = p[1]
	# print "check:comp ", p[0]
	if(p[2]!=None):
		p[0].code += p[2].code

def p_stmts(p):
	'''stmts : stmts terminals expr
			 | stmt'''
	
	if(len(p)==4):
		p[0]=p[1]
		# print "checks of error",p[0].code, p[2].code, p[3].code 
		p[0].code += p[2].code + p[3].code
	else:
		p[0]=p[1]
	# print "check: stmts", p[0]

def p_stmt(p):
	'''stmt : expr
			| call DO compstmt END
			| stmt IF expr
			| stmt WHILE expr
			| stmt UNLESS expr
			| stmt UNTIL expr
			| BEGIN LCBRACKET compstmt RBRACKET
			| END LCBRACKET compstmt RBRACKET
			| lhs EQUAL command
			| lhs EQUAL command do compstmt END'''
	if(len(p)==2):
		p[0]=p[1]

def p_expr(p):
	'''expr : mlhs EQUAL mrhs
			| RETURN call_args
			| expr AND expr
			| expr OR expr
			| NOT expr
			| command
			| LOGICAL_NOT command
			| args'''
	if(len(p)==2):
		p[0]=p[1]
		# print "check:expr",p[0].code

def p_call(p):
	'''call : function
			| command'''
	p[0]=p[1]

def p_command(p):
	'''command : primary DOT variable call_args'''
	p[0]=["command"]
	for i in range(1,len(p)):
		p[0].append(p[i])
 	
def p_function(p):
	'''function : variable LPARENTHESIS call_args RPARENTHESIS
				| primary DOT variable LPARENTHESIS call_args RPARENTHESIS
				| primary DOT variable
				| primary DOUBLECOLON variable'''
	p[0]=["function"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_arg(p):
	'''arg : lhs EQUAL arg
		   | lhs op_asgn arg
		   | arg DOUBLEDOT arg
		   | arg PLUS arg
		   | arg MINUS arg
		   | arg MULTIPLY arg
		   | arg DIVIDE arg
		   | arg REMAINDER arg
		   | arg EXPONENT arg
		   | arg BINARY_OR arg
		   | arg BINARY_XOR arg
		   | arg BINARY_AND arg
		   | arg COMPARISON arg
		   | arg GREATER_THAN arg
		   | arg GREATER_THAN_EQ arg
		   | arg LESS_THAN arg
		   | NOT arg
		   | arg LESS_THAN_EQ arg
		   | arg EQUALS arg
		   | arg NOT_EQUALS arg
		   | arg LOGICAL_NOT arg
		   | arg BINARY_LSHIFT arg
		   | arg BINARY_RSHIFT arg
		   | arg LOGICAL_AND arg
		   | arg LOGICAL_OR arg
		   | primary'''
	checkcount=1
	# print checkcount
	checkcount += 1
	if(len(p)==4):
		if(p[2]==".."):
			# print "doule dot niggers *******************8"
			p[0]=Node()
			p[0].place=p[1].place
			p[0].place2=p[3].place
			print p[0]
		elif(p[2] in ['+','-','/','*','%','^','|','<<','>>','&','&&','||',"<=","<",">=",">","==","!="]):
			print "latest check,",p[1],p[1].code,p[1].type,p[1].place
			if(p[1].type):
				temp = st.newtemp(p[1].type)
			else:
				temp = st.newtemp(st.gettype(p[1]))	
			# print "check arg p1 ",p[1].code
			# print "check arg p3 ",p[3].code
			p[0]=Node()
			p[0].code = p[1].code + p[3].code
			p[0].place = temp
			p[0].type=p[1].type
			# if(not st.lookup(p[1].place)):
			# 	print "error. variable, "+ p[1].place +" value not assigned before"
			# 	sys.exit()
			# if(not st.lookup(p[3].place)):
			# 	print "error. variable, "+ p[3].place +" value not assigned before"
			# 	sys.exit()
			if(p[2] in ["<=","<",">=",">","==","!="]):
				# print "did the big stuff"
				lab1 = st.newlabel()
				lab2 = st.newlabel()
				p[0].code += ["ifgoto, ",relop[p[2]]+", "+p[1].place+", "+p[3].place+", "+lab1+" \n"]
				p[0].code += ["=, "+p[0].place+", 0 \n"]
				p[0].code += ["goto, "+lab2+" \n"]
				p[0].code += [lab1+": \n"]
				p[0].code += ["=, "+p[0].place+", 1 \n"]
				p[0].code += [lab2+": \n"]
			else:	
				p[0].code += [p[2]+", "+p[0].place+", "+p[1].place+", "+p[3].place+" \n"]
		elif(p[2]=='='):
			p[0]=Node()
			print "updating type of",p[1].place,p[3].type
			p[1].type = p[3].type
			if(not st.lookup(p[1])):
				print "type insertion is", p[3].type, "for ",p[1].place
				st.insert(p[1].place,p[3].type)
			try:
				float(p[3].place)
			except:
				if(p[3].type == "variable" and (not st.lookup(p[3].place))):
					print "error. variable, "+ p[3].place +" value not assigned before"
					sys.exit()
			# print "check arg p1 ",p[1].code
			# print "check arg p3 ",p[3].code
			# print "concatenating", ''.join([p[2]]+[", "]+[p[1].place]+[", "]+[p[3].place])
			p[0].code = p[1].code + p[3].code
			p[0].code += [p[2]+", "+p[1].place+", "+p[3].place+" \n"]
			p[0].type = p[3].type
	elif(len(p)==2):
		p[0] = p[1]
		print "type of arg", p[0].place, p[0].type
	elif(len(p)==3):
		temp = st.newtemp("bool")
		p[0]=Node()
		p[0].place=temp
		if(not st.lookup(p[2].place)):
				print "error. variable, "+ p[2].place +" value not assigned before"
				sys.exit()
		p[0].code += ["not, "+p[0].place+", "+p[2].place+" \n"]
		p[0].type = "bool"
	# print "check: arg", ''.join(p[0].code)

def p_opt_elsifstmt(p):
	'''opt_elsifstmt : ELSIF expr then compstmt opt_elsifstmt
					 | none'''
	if(len(p)==6):
		lab1=st.newlabel()
		p[0]=Node()
		p[0].label=lab1
		p[0].code += [p[0].label,": \n"]
		p[0].code += p[2].code
		p[0].type="elifcode"
		if(p[5]):
			p[0].code += ["ifgoto, eq, "+ p[2].place+ ", 0, "+p[5].label+" \n"]
		else:
			p[0].code += ["ifgoto, eq, "+ p[2].place+ ", 0, "+st.getelabel()+" \n"]
		p[0].code += p[4].code
		p[0].code += ["goto, "+st.getalabel()+"\n"]
		if(p[5]):
			p[0].code += p[5].code
		print "check from elsif:",p[0].code
	else:
		p[0]=None



def p_opt_elsestmt(p):
	'''opt_elsestmt : ELSE compstmt
					| none'''
	if(len(p)==3):	
		p[0]=p[2]
		print "check from else: ",p[0].code


def p_primary(p):
	'''primary : LPARENTHESIS compstmt RPARENTHESIS
				 | variable
				 | literal
				 | primary LBRACKET opt_args RBRACKET
				 | LBRACKET opt_args RBRACKET
				 | LCBRACKET opt_args RCBRACKET
				 | RETURN 
				 | RETURN LPARENTHESIS call_args RPARENTHESIS
				 | function
				 | IF expr then compstmt opt_elsifstmt opt_elsestmt END
				 | UNLESS expr then compstmt opt_elsestmt END
				 | WHILE expr do compstmt END
				 | UNTIL expr do compstmt END
				 | CASE compstmt WHEN when_args then compstmt opt_when_args opt_elsestmt END
				 | FOR block_var IN expr do compstmt END
				 | BEGIN compstmt END
				 | CLASS variable terminals compstmt END
				 | DEF fname argdecl compstmt END'''
	if(len(p)==2):
		if(p[1]!='return'):
			p[0]=p[1]
			p[0].place = p[1].place
			p[0].type = p[1].type
			print "typye in primary of ",p[0].place, p[0].type
	elif(p[1]=="while"):
		lab1 = st.newlabel()
		lab2 = st.newlabel()
		p[0]=Node()
		p[0].code += [lab1+": \n"]
		p[0].code += p[2].code
		p[0].code += ["ifgoto, eq, "+ p[2].place+ ", 0, "+lab2+" \n"]
		p[0].code += p[4].code
		p[0].code += ["goto, "+lab1+"\n"]
		p[0].code += [lab2+": \n"]
		p[0].type="while"
	elif(p[1]=="if"):
		alabel=st.afterlabel()
		elabel=st.elselabel()
		p[0]=Node()
		p[0].code += p[2].code
		if(p[5]):
			p[0].code += ["ifgoto, eq, "+ p[2].place+ ", 0, "+p[5].label+" \n"]
		else:
			p[0].code += ["ifgoto, eq, "+ p[2].place+ ", 0, "+elabel+" \n"]
		p[0].code += p[4].code
		p[0].code += ["goto, "+alabel+"\n"]
		if(p[5]):
			p[0].code += p[5].code
		p[0].code += [elabel+": \n"]
		if(p[6]):
			p[0].code += p[6].code
		p[0].code += [alabel+": \n"]
	elif(p[1]=="for"):
		lab1 = st.newlabel()
		p[0]=Node()
		if(not st.lookup(p[2])):
				print "inserted ",p[2].place
				st.insert(p[2].place,p[4].type)
		try:
			int(p[4].place)
		except:
			if(not st.lookup(p[4].place)):
				print "error. variable, "+ p[4].place +" value not assigned before"
				sys.exit()
		p[0].code += ["=, "+p[2].place+", "+p[4].place+" \n"]
		p[0].code += [lab1+": \n"]
		p[0].code += p[6].code
		p[0].code += ["+, ",p[2].place+", "+p[2].place+", 1\n"]
		p[0].code += ["ifgoto, leq, "+ p[2].place+ ", "+p[4].place2+", "+lab1+" \n"]
		p[0].code="for"
	elif(p[1]=="("):
		p[0]=p[2]

def p_opt_when_args(p):
	'''opt_when_args  : WHEN when_args then compstmt opt_when_args
					  | none'''
	p[0]=["opt_when_args"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_opt_argstuff(p):
	'''opt_argstuff : opt_argstuff COMMA MULTIPLY arg
					| none'''
	p[0]=["opt_argstuff"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_when_args(p):
	'''when_args : args opt_argstuff
				 | MULTIPLY arg'''
	p[0]=["when_args"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_then(p):
	'''then : terminals
	        | THEN
	        | THEN terminals'''
	p[0]=["then"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_do(p):
	'''do : terminals
	        | DO
	        | terminals DO'''
	p[0]=["do"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_block_var(p):
	'''block_var : mlhs'''
	p[0]=p[1]
#########################################
def p_opt_mlhs(p):
	'''opt_mlhs : COMMA mlhs_item opt_mlhs
				| none'''


def p_mlhs(p):
	'''mlhs : mlhs_item opt_mlhs'''
	p[0]=p[1]
	if(p[2]):
		p[0].code += p[2].code

#########################################


def p_mlhs_item(p):
	'''mlhs_item : lhs'''
	p[0]=p[1]

def p_lhs(p):
	'''lhs : variable
	       | primary DOT variable
	       | NIL'''
	if(len(p)==2):
		p[0]=p[1]
		p[0].place = p[1].place

	# print "check: lhs", p[0].code

def p_mrhs(p):
	'''mrhs : args opt_argstuff
			| MULTIPLY arg'''
	p[0]=["mrhs"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_opt_call_args(p):
	'''opt_call_args : call_args
					 | none'''
	p[0]=["opt_call_args"]
	for i in (1,len(p)):
		p[0].append(p[i])

# def p_opt_bcall_args(p):
# 	'''opt_bcall_args : LPARENTHESIS call_args RPARENTHESIS
# 					  | none'''
# 	p[0]=["opt_bacll_args"]
# 	for i in range(1,len(p)):
# 		p[0].append(p[i])

# def p_opt_argstuff2(p):
# 	'''opt_argstuff2 : opt_argstuff2 COMMA BINARY_AND arg
# 	                | none'''
# 	p[0]=["opt_argstuff2"]
# 	for i in range(1,len(p)):
# 		p[0].append(p[i])

def p_call_args(p):
	'''call_args : call_args COMMA call_args
				 | MULTIPLY arg
				 | BINARY_AND arg
				 | arg
				 | command
				 | none'''
	p[0]=["call_args"]
	for i in range(1,len(p)):
		p[0].append(p[i])



def p_opt_args(p):
	'''opt_args : args
	            | none'''
	p[0]=p[1]


def p_args(p):
	'''args : arg
			| args COMMA arg'''
	if(len(p)==2):
		p[0]=p[1]

def p_argdecl(p):
	'''argdecl : LPARENTHESIS arglist RPARENTHESIS opt_terminals
			   | arglist terminals'''
	p[0]=["argdecl"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_opt_variables(p):
	'''opt_variables : COMMA variable opt_variables
			   | COMMA MULTIPLY variable opt_variables
			   | COMMA BINARY_AND variable opt_variables
			   | none'''
	p[0]=["opt_variables"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_arglist(p):
	'''arglist : variable opt_variables
			   | MULTIPLY variable opt_variables
			   | BINARY_AND variable opt_variables
			   | none'''
	p[0]=["arglist"]
	for i in range(1,len(p)):
		p[0].append(p[i])


# def p_variable(p):
# 	'''variable : varname'''
# 	p[0]=["variable"]
# 	for i in range(1,len(p)):
# 		p[0].append(p[i])

def p_literal(p):
	'''literal : INTNUMBER
			   | FLOATNUMBER
			   | STRING'''
	p[0]=Node()
	p[0].place=p[1]
	print "literal, ",p[1],"type ",type(p[1])
	p[0].type=type(p[1])
	if(p[0].type=="string"):
		print "yess"
		p[0].place=str('\''+p[1]+'\'')

def p_op_asgn(p):
	'''op_asgn : PLUS_EQ
			   | MINUS_EQ
			   | MULTIPLY_EQ
			   | DIVIDE_EQ
	           | REMAINDER_EQ
               | EXPONENT_EQ
               | BINARY_OR_EQ
               | BINARY_XOR_EQ
               | BINARY_AND_EQ
               | BINARY_LSHIFT_EQ
               | BINARY_RSHIFT_EQ
               | LOGICAL_AND_EQ
               | LOGICAL_OR_EQ'''
	p[0]=["op_asgn"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_fname(p):
	'''fname : variable'''
	p[0] = p[1]

# def p_operation(p):
# 	'''operation : variable'''
# 	p[0]=["operation"]
# 	for i in range(1,len(p)):
# 		p[0].append(p[i])

# def p_varname(p):
# 	'''varname : global
# 			   | variable'''
# 	p[0]=["varname"]
# 	for i in range(1,len(p)):
# 		p[0].append(p[i])

def p_variable(p):
	'''variable : VARIABLE
			    | DOLLAR VARIABLE'''
	if(len(p)==2):
		p[0]=Node()
		p[0].place=p[1]
		p[0].type="variable"
		if(st.lookup(p[1])):
			p[0].type=st.gettype(p[1])
	else:
		p[0]=Node()
		p[0].place=str(p[1])+str(p[2])
		p[0].type="variable"
		if(st.lookup(p[2])):
			p[0].type=st.gettype(p[2])
	# print "type of from variabl",p[0].place,p[0].type
	

def p_none(p):
	'''none :'''
	p[0]=Node()


def p_terminals(p):
	'''terminals : SEMICOLON
				 | NEWLINE'''
	p[0]=Node()
	p[0].place="newline"

def p_opt_terminals(p):
	'''opt_terminals : terminals
					 | none'''
	p[0] = p[1]
		 
# def p_error(p):
# 	print "Syntax error"

yacc.yacc()

data = ""
with open(filename,'r') as myfile:
	for line in myfile.readlines():
		if line!='\n':
			data = data + line

result = yacc.parse(data)
# print
# printRightDeriv(result)
