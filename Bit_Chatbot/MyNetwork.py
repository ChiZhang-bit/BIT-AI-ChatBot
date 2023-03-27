from torch.nn import *
import torch


class MyNetwork(Module):
    def __init__(self) -> None:
        super().__init__()

        # Network Construct
        self.module = Sequential(
            Conv2d(in_channels=3, out_channels=32, kernel_size=5, padding=2),
            MaxPool2d(kernel_size=2),
            Conv2d(in_channels=32, out_channels=32, kernel_size=5, padding=2),
            MaxPool2d(kernel_size=2),
            Conv2d(in_channels=32, out_channels=64, kernel_size=5, padding=2),
            MaxPool2d(kernel_size=2),
            Flatten(),
            Linear(4096, 64),
            ReLU(),
            Linear(64, 2)
        )

    def forward(self, x):
        x = self.module(x)
        return x
