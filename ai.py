import torch
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
from torchvision.utils import save_image
import sys
import time

class VGG19(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = models.vgg19(weights="IMAGENET1K_V1")
    def forward(self, x):
        features = []
        layers = [0,5,10,19,28]
        for i,layer in enumerate(self.model.features[:30]):
            x = layer(x)
            if i in layers:
                features.append(x)
        return features

def Gram(A):
    B = A.view(A.shape[1], -1)
    return torch.mm(B, B.t())

def rgba_to_rgb(url):
    img = Image.open(url)
    img2 = img.convert("RGB")
    img2.save(url)

def img_to_tensor(url, device, height, width):
    transform = transforms.Compose([
        transforms.Resize(size=(height,width)),
        transforms.ToTensor()
    ])
    return transform(Image.open(url)).unsqueeze(0).to(device)

def tensor_to_img(generated, epoch):
    tensor = generated.clone()
    tensor = tensor.squeeze()
    save_image(tensor, f'generated{epoch}.png')

class NSTLoss(nn.Module):
    def __init__(self):
        super().__init__()
    
    def forward(self, C, S, G, alpha, beta, lambd):
        content_loss = torch.mean((C[3]-G[3]) ** 2)
        style_loss = 0
        for i in range(5):
            G_gram = Gram(G[i])
            S_gram = Gram(S[i])
            style_loss += lambd[i] * (torch.norm(S_gram-G_gram, p='fro'))
        loss = alpha * content_loss + beta * style_loss
        return loss
    
def custom_img(url1, url2):

    device = 'cpu'
    if torch.cuda.is_available():
        device = 'cuda'
    model = VGG19().to(device).eval()
    height = 300
    width = 400
    content = img_to_tensor(url1, device, height, width)
    style = img_to_tensor(url2, device, height, width)
    generated = content.clone().requires_grad_(True).to(device)

    content_feat = model(content)
    content_feat = [feat.detach() for feat in content_feat]
    style_feat = model(style)
    style_feat = [feat.detach() for feat in style_feat]

    lr = 0.003
    alpha = 10
    beta = 100
    lambd = [0 for i in range(5)]
    lambd[0] = 1
    lambd[1] = .8
    lambd[2] = .7
    lambd[3] = .2
    lambd[4] = .1
    criterion = NSTLoss()
    optimizer = optim.Adam([generated], lr=lr)

    epochs = 3

    for epoch in range(epochs):
        generated_feat = model(generated)
        optimizer.zero_grad()
        loss = criterion(content_feat, style_feat, generated_feat, alpha, beta, lambd)
        loss.backward()
        optimizer.step()
        if epoch == 0:
            print("Generating!")
        tensor_to_img(generated, epoch)