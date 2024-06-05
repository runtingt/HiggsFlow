class Model:
    def __init__(self, channel: str, model: str, scan_method: str, 
                 type_string: str, attribute_string: str):
        self.channel = channel
        self.model = model
        self.scan_method = scan_method
        self.types = type_string
        self.attributes = attribute_string
        
    def to_params(self):
        return {
            "channel": self.channel,
            "model": self.model,
            "scan_method": self.scan_method,
            "types": self.types,
            "attributes": self.attributes
        }
        
models = {
    'hgg_statonly2D_grid': Model('hgg_statonly', 'STXStoSMEFTExpandedLinearStatOnly', 'grid', 'observed', 'nominal'),
    'hgg_statonly2D_rand': Model('hgg_statonly', 'STXStoSMEFTExpandedLinearStatOnly', 'rand', 'observed', 'nominal'),
}
