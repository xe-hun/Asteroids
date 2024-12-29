class SaveDataModel:
    
    _best_level_key = 'best_level'
    
    def __init__(self, best_level:int):
        self.best_level = best_level
        
    @staticmethod 
    def initial():
        return SaveDataModel(1)
        
    @staticmethod
    def from_dict(data:dict):
        if data == None:
            return SaveDataModel.initial()
        return SaveDataModel(data[SaveDataModel._best_level_key])
    
    def to_dict(self):
        return {
            SaveDataModel._best_level_key : self.best_level
        }
    # def from_jso
