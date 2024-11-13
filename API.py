class Remedio():
    def __init__(self):
        self.nomeRemedio = 0
        self.descricaoRemedio = 0
        self.horarioRemedio = 0
        self.dosagemRemedio = 0
        
    def nome (self,Nome):
        self.nomeRemedio = Nome
    
    def descricao(self,descricao):
        self.descricaoRemedio = descricao
    
    def horario(self,horario):
        self.horarioRemedio = horario
        
    def dosagem(self,dosagem):
        self.dosagemRemedio = dosagem
        
    def infoRemedio(self):
        info = [[]]
        info[0].append(self.nomeRemedio)
        info[0].append(self.descricaoRemedio)
        info[0].append(self.horarioRemedio)
        info[0].append(self.dosagemRemedio)
        
        return info
        
    def infoNome(self):
        return self.nomeRemedio
        
    def infoDescricao(self):
        return self.descricaoRemedio
        
    def infohorario(self):
        return self.horarioRemedio
        
    def infoDose(self):
        return self.dosagemRemedio
    