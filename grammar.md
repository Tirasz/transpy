```gf
lit_constant = Constant(value val)  
	     | UnaryOp(USub(), Constant(value val))

subject = Name(identifier id, expr_context Load)


LiteralExpression(subject subj) = Compare(lit_constant left, ops = [Eq], comparators = [subj])
       				| Compare(left = subj, ops = [Eq], comparators = [lit_constant])

LiteralTestBase(subject subj) = LiteralExpression(subject = subj)
			      | BoolOp(op = Or, values = [LiteralExpression(subject = subj), LiteralExpression(subject = subj)+]
  		          
LiteralTest(subject subj) = LiteralTestBase(subject = subj)
			  | BoolOp(op = And, values=[LiteralTestBase(subject = subj)+, expr+ expressions]

LiteralCase(subject subj) = If(test = LiteralTest(subject=subj), stmt* body, LiteralTest(subject = subj)+ orelse)


semi_lit_op = Lt | LtE | Gt | GtE | NotEq | Eq

semi_lit_bool = Or | And

Semi-LiteralExpression(subject subj) = Compare(lit_constant left, ops = [semi_lit_op], comparators = [subj])
       				     | Compare(left = subj, ops = [semi_lit_op], comparators = [lit_constant])

Semi-LiteralTest(subject subj) = Semi-LiteralExpression(subject = subj)
			       | BoolOp(op = semi_lit_bool, values = [Semi-LiteralExpression(subject = subj)+, expr+ expressions])

Semi-LiteralCase(subject subj) = If(test = Semi-LiteralTest(subject=subj), stmt* body, Semi-LiteralTest(subject = subj)+ orelse)

```
