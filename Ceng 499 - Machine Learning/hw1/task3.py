import torch
import torch.nn as nn
import torch.nn.functional as F


class MyModel(nn.Module):
  num_channels = 1
  num_outputs = 10

  def __init__(self):
    super().__init__()
    self.conv1 = nn.Conv2d(1, 1, 5, 1)
    self.conv2 = nn.Conv2d(1, 1, 5, 1)
    self.fc1 = nn.Linear(784, 500)
    self.fc2 = nn.Linear(500, num_outputs)

  def forward(self, x):
    x = F.relu(self.conv1(x))
    x = nn.AdaptiveAvgPool2d((28,28))(x)
    x = F.relu(self.conv2(x))
    x = nn.AdaptiveAvgPool2d((28,28))(x)
    x = torch.flatten(x, 1)
    x = F.relu(self.fc1(x))
    x = self.fc2(x)
    return x
