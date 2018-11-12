class Id:
    ident = 0
    @staticmethod
    def getNew():
        Id.ident +=1
        return Id.ident