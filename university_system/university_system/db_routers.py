class DatabaseRouter:
    """
    A router to control all database operations on models in the
    student_service and professor_service applications.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'student_service':
            return 'default'
        elif model._meta.app_label == 'professor_service':
            return 'professor_service'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'student_service':
            return 'default'
        elif model._meta.app_label == 'professor_service':
            return 'professor_service'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'student_service':
            return db == 'default'
        elif app_label == 'professor_service':
            return db == 'professor_service'
        return None