import torch

def load_model(path: str):
    model = torch.load(path)
    test_X = torch.tensor([[0.0] * 10], dtype=torch.float32)
    model.encoder(test_X)
    return model