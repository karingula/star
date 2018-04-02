# print("left_type:",type(k.left),"right_type:", type(k.right.key))
# print("left:",k.left,"right:", k.right.key)
#print(type(sample))



# print("Normal Inspection:", pk_list)
#
# #  Ripping __table_args__ apart for clear understanding
# for z in Flight.__table_args__:
#     # Each item of __table_args__ is an UniqueConstraint object
#     # UniqueConstraint object inherits ColumnCollection object
#     # ColumnCollection object inherits util.OrderedProperties object
#     # OrderedProperties object inherits Properties object
#     print(type(z))
#     #__visit_name__, columns are properties of a Properties object
#     print(z.__visit_name__)
#     # columns is a ColumnCollection object which is iterable
#     print(type(z.columns))
#     for y in z.columns:
#         # Each element of ColumnCollection object is a Column object from schema
#         # ex: <class 'sqlalchemy.sql.schema.Column'>
#         print(type(y))
#         #name is the property of Column object which gives the name of the Column of SQLAlchemy model
#         print(y.name)
#     col_list = tuple([k.name for k in z.columns.__iter__()])
#     print("This is col list:",col_list)
#



# #create a dataframe
# list1 = [1, ('Vanc','ouver', 'Canada'), 'Toronto', '3-Jan']
# list2 = [2, ('Amst','erdam', 'Netherlands'), None, '15-Feb']
# list3 = [4, None, 'Glasgow', '12-Jan']
# list4 = [9, ('Halm','stad', 'Norway'), 'Athens', '21-Jan']
# list5 = [3, ('Bris','bane', 'Australia'), 'Toronto', None]
# list6 = [4, ('Johan','nesburg', 'South Africa'), 'Venice', '12-Jan']
# list7 = [9, None, None, '20-Oct']
# data = [list1,list2,list3,list4,list5,list6,list7]
# df = pd.DataFrame(data, columns=['flight_id','from_location','to_location','schedule'])
#
# violation_checker = service.Violation()
#
# #get all the columns which violated the unique constraints
# uc_violations = list(map(functools.partial(violation_checker.fetch_violation_records_uniqueness, df=df), uc_cols))
# print("UC_Violations",uc_violations)
# # get all the columns which violated the primary key constraints
# pk_violations = list(map(functools.partial(violation_checker.fetch_violation_records_uniqueness, df=df), pk_cols))
# print("PK Violations:", pk_violations)
# nul_cols = [col.name for col in Flight.__table__.columns if not col.nullable]
# # print("Nullable Cols:",nul_cols)
# nul_violations = violation_checker.fetch_violation_records_nullable(df=df,cols=nul_cols)
# print("Nullable Violations:", nul_violations)

# a_list format is [Model.column == df.record.value]
# # a_list = [Flight.to_location=='Vancouver', Flight.from_location=='Boston']
# # b_list = [Flight.schedule == '2018-07-20',and_(*a_list)]
# # k = Flight.to_location=='Toronto'
# print(type(Flight.__table__.columns))
# a_list = []
# for col_tuple in uc_cols:
#    print(col_tuple)
#    #for each tuple build and_ BinaryExpression
# for c in Flight.__table__.columns:
#    print(type(c=='vancouver'))
# #print(BinaryExpression(Flight.to_location, 'Toronto', '__eq__'))
# #z = session.query(Flight).filter(or_(*b_list)).first()
# """
# k:-
# Description: object of type BinaryExpression
# Properties: left, right, operator, type, negate
#
# left:-
# Description: object of type AnnotatedColumnElement.
# Properties: name, key, table
#
# right:-
# Description: object of type BindParameter
# Properties: value(type: str), key(type: _anonymous_label), required(type: bool)
# """
# #
