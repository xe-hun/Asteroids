class SaveDataModel:
    
    _best_level_key = 'high_score'
    
    def __init__(self, high_score:int):
        self.high_score = high_score
        
    @staticmethod 
    def initial():
        return SaveDataModel(0)
        
    @staticmethod
    def from_dict(data:dict):
        if data == None:
            return SaveDataModel.initial()
        return SaveDataModel(data.get(SaveDataModel._best_level_key, 0))
    
    def to_dict(self):
        return {
            SaveDataModel._best_level_key : self.high_score
        }
    # def from_jso
