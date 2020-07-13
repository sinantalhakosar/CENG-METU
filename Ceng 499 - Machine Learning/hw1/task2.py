import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(1234)

class MyModel1(nn.Module):
    num_features = 32 * 32 * 3
    num_categories = 10
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(MyModel1.num_features, 750)
        self.fc4 = nn.Linear(750, MyModel1.num_categories)

    def forward(self, x):
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = self.fc4(x)
        return x

class MyModel2(nn.Module):
    num_features = 32 * 32 * 3
    num_categories = 10
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(MyModel2.num_features, 750)
        self.fc2 = nn.Linear(750, 200)
        self.fc3 = nn.Linear(200, MyModel2.num_categories)

    def forward(self, x):
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class MyModel3(nn.Module):
		num_features = 32 * 32 * 3
		num_categories = 10
		def __init__(self):
			super().__init__()
			self.fc1 = nn.Linear(MyModel3.num_features, 750)
			self.fc2 = nn.Linear(750, 200)
			self.fc3 = nn.Linear(200, 50)
			self.fc4 = nn.Linear(50, MyModel3.num_categories)

		def forward(self, x):
			x = torch.flatten(x, 1)
			x = F.relu(self.fc1(x))
			x = F.selu(self.fc2(x))
			x = F.selu(self.fc3(x))
			x = self.fc4(x)
			return x

device = "cuda" # cpu by default

import torchvision.transforms as transforms
from torchvision.datasets import CIFAR10

ratio = 0.1
transform = transforms.Compose(
    [transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

train_set = CIFAR10(root="task2_data", train=True, transform=transform, download=True)
test_set = CIFAR10(root="task2_data", train=False, transform=transform, download=True)

train_set, val_set = torch.utils.data.random_split(train_set, [int((1 - ratio) * len(train_set)), int(ratio * len(train_set))])
batch_size = 1000
train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size)

def layer(layer_count=1):
    if layer_count == 1:
        model = MyModel1().to(device)
        num_epochs = 12
    elif layer_count == 2:
        model = MyModel2().to(device)
        num_epochs = 13
    else:
        model = MyModel3().to(device)
        num_epochs = 11
    my_loss = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

    
    for epoch in range(num_epochs):
        sum_loss = 0
        for i, (images, labels) in enumerate(train_loader):
            images = images.to(device)
            labels = labels.to(device)

            output = model(images)
            loss = my_loss(output, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            sum_loss += loss.item()


        print('Epoch [%d] Train Loss -[%d] layer: %.4f'% (epoch+1,layer_count, sum_loss/i))

        with torch.no_grad():
            correct = total = 0
            for images, labels in test_loader:
                images = images.to(device)
                labels = labels.to(device)

                output = model(images)
                _, predicted_labels = torch.max(output, 1)
                correct += (predicted_labels == labels).sum()
                total += labels.size(0)
            print('Percent correct - [%d] layer: %.3f %%' % (layer_count,(100 * correct) / (total + 1)))

layer(1)
layer(2)
layer(3)
