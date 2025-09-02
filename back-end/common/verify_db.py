def verificarSetupDB(db):
    """Verificar si la conexión a base de datos funciona"""
    try:
        with db.engine.connect() as conn:
            print('funciona')
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tablas = inspector.get_table_names()

        if 'user' in tablas:
            print('Tabla "user" encontrada')
            return True
        else:
            print('Tabla no encontrada')
            return False
    except Exception as e:
        print(f'Error en setup de DB: {e}')
        return False
