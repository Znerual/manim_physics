class Id_generator:
    counter: int = 0

    @staticmethod
    def get_new_id():
        Id_generator.counter += 1
        return Id_generator.counter