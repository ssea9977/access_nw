import sys
import os
import pandas as pd 
from sqlalchemy import create_engine

def match_info( info_name, num ) :
    global db_list
    num = int( num )
    if info_name == 'get_host' :
        host_list = [ '172.21.27.207', '172.21.27.208', '172.21.27.209', '172.21.27.128', '172.21.27.129'  ]
        return host_list[ num - 1 ]
    elif info_name == 'get_db' :
        return db_list[ num - 1 ]

def get_user_pw( host ) :
    if host == '172.21.27.128' :
        user = 'aison'
    else :
        user = 'root'
    pw = 'Rkdqnrlte1q'
    return user, pw

def get_db_list() :
    global host, user, pw, db, db_list
    db_list = []
    eng = create_engine('mysql+pymysql://' + user + ':' + pw + '@' + host + ':3306', pool_recycle=3600)
    q = eng.execute('SHOW DATABASES')
    available_db = q.fetchall()
    print( '\n***** DB *****' )
    for i in range( len( available_db ) ) :
        print( ' ', i + 1, ': ', available_db[ i - 1 ][ 0 ] )
        db_list.append( available_db[ i - 1 ][ 0 ] )

def get_table_list( yn ) :
    global host, user, pw, db, talbe_list
    if yn == 'y' :
        eng = create_engine('mysql+pymysql://' + user + ':' + pw + '@' + host + ':3306' + '/' + db , pool_recycle=3600)
        print( eng.table_names() )
    else :
        pass

def print_warning( str_warn ) :
    print()
    print( '!!!!!!!!!!!! WRONG ' + str_warn + ' !!!!!!!!!!!!' )
    print()

def undo( cmd ) :
    if cmd.lower() == 'u' :
        return True

def exit_pg( cmd ) :
    if cmd.lower() == 'e' :
        print( '\n======= BYE =======' )
        sys.exit()

def check_num( info_name, num ) :
    global host_list, db_list
    try :
        num = int( num )
        if info_name == 'get_host' :
            if num < 1 or num > 5 :
                return True
            else:
                return False
        elif info_name == 'get_db' :
            if num < 1 or num > len( db_list ) :
                return True
            else:
                return False
    except :
        return True

def input_host() :
    global host, db, user, pw
    print( "\n[ EXIT : 'e' or 'E' ]" )
    host_num = input( '***** HOST ***** \n 1: 207 / 2: 208 / 3: 209 / 4: 128 / 5: 129 \nhost >>> ' )
    exit_pg( host_num )
    while check_num( 'get_host',  host_num ) :
        print_warning( 'MUMBER' )
        print( "\n[ EXIT : 'e' or 'E' ]" )
        host_num = input( '***** HOST ***** \n 1: 207 / 2: 208 / 3: 209 / 4: 128 / 5: 129 \nhost >>> ' )
        exit_pg( host_num )
        check_num( 'get_host', host_num )
    host = match_info( 'get_host', host_num )
    user, pw = get_user_pw( host )

def input_db() :
    global host, db, user, pw, db
    get_db_list()
    print( "\n[ EXIT : 'e' or 'E' ]\n[ UNDO : 'u' or 'U' ]" )
    db_num = input( 'DB >>> ' )
    if undo( db_num ) :
        return True
    exit_pg( db_num )
    while check_num( 'get_db', db_num ) :
        print_warning( 'MUMBER' )
        print( "\n[ EXIT : 'e' or 'E' ]\n[ UNDO : 'u' or 'U' ]" )
        db_num = input( 'DB >>> ' )
        if undo( db_num ) :
            return True
        exit_pg( db_num )
        check_num( 'get_db', db_num )
    db = match_info( 'get_db', db_num ) 
    print( '\n===== SELECT: ' + db + ' =====' )
    get_table_yn = input( '\nWANNA SHOW TABLES? (y/n) >>> ' ).lower()
    print( '\n======= ' + db.upper() + ' TABLE LIST =======' )
    get_table_list( get_table_yn )

def input_query() : 
    global query
    print( "\n[ EXIT : 'e' or 'E' ]\n[ UNDO : 'u' or 'U' ]" )
    query = input( '***** QUERY ***** \nquery >>> ' )  
    if undo( query ) :
        return True
    exit_pg( query ) 
    while True :
        try :
            df = sqlalchemy_connector( host, db, user, pw, query )
            break
        except :
            print_warning( 'QUERY' )
            print( "\n[ EXIT : 'e' or 'E' ]\n[ UNDO : 'u' or 'U' ]" )
            query = input( '\n***** QUERY ***** \nquery >>> ' )
            if undo( query ) :
                return True
            exit_pg( query ) 

def get_file( df ) :
    file_name = input( '\nfile name >>> ' )
    print( '\n===== YOUR FILE NAME IS [ {} ] ====='.format( file_name ) )
    file_name_yn = input( 'ARE YOU SURE? (y/n) >>> ' ).lower()
    while file_name_yn == 'n' :
        file_name = input( 'file name >>> ' )
        print( '\n===== YOUR FILE NAME IS [ {} ] ====='.format( file_name ) )
        file_name_yn = input( 'ARE YOU SURE? (y/n) >>> ' ).lower()

    file_type = int( input( '\n***** FILE TYPE ***** \n 1: csv / 2: excel >>> ' ) )
    while True :
        if file_type == 1 :
            df.to_csv( '/home/aison/export_data/data/' + file_name + '.csv', encoding = 'euc-kr', index = False )
            break
        elif file_type == 2 :
            df.to_excel( '/home/aison/export_data/data/' + file_name + '.xlsx', encoding = 'euc-kr', index = False )
            break
        else :
            print_warning( 'NUMBER' )
            file_type = int( input( '\n***** FILE TYPE ***** \n 1: csv / 2: excel >>> ' ) )

def sqlalchemy_connector( host, db, user, pw, sql ):
    engine = create_engine( 'mysql+pymysql://' + user + ':' + pw + '@' + host + ':3306/' + db )
    df = pd.read_sql_query( sql, engine )
    return df

if __name__ == "__main__" :
    global host, db, user, pw, query, file_name, cmd_list
    cmd_list = [ input_host, input_db, input_query ]

    i = 0
    while i > -1 and i < 3  :
        if cmd_list[ i ]() :
            i -= 1
        else:
            i += 1
        
    df = sqlalchemy_connector( host, db, user, pw, query )
    get_file( df )



