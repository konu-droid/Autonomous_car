'''
1. Had many problems with detach() and memory filling cause i had to set retain_gragh=true for the RNN to work
else it could not do the backwards step since the last pass was missing for the second iteration but i used 
detach() to remove the weights every iteration, i was not satisfied with that so down below is the way i implemented
my rnn, by using two rnn so the first pass is just to generate the hidden and the next one learns the network

2. Had many problems with half precission, when running on full precision it was workiing fine
but as soon as i started using half precision it started oing into nan for loss function
i changed the epsilon too but to no use,
and on full precision gpu ram was too small to fit everything undesirable network size
read on many fofum about changeing epsilon and all
plus also i am just using half for the network when doing the optimizer step i am coverting to full 
cause otimizser was causeing a lot of problems at half too 
still i was getting nan's after the first step, so then i saw my learning rate was too high it was 0.1
when i fixed that to 0.001 everything is working fine for now
so he problem was that the model learned too fast and the weights and bias went into nan's states 
so now i will make sure it update slow and also using leaky relu could have helped a lot too

3. when the learning rate was high, relu allowed the values to become infinite and then nan,
so a normalization was required

4. Tried to use convolutional layers as well along with rnn but, the result were not good insce the GPU doesnt have much 
space for that, convolution basically works by creating features maps it dont just compress image, it compresses image
but it also need a lot of these compressed images ( feature maps ) to work its magic, cant work with just one feature map
'''

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch import autograd

import cv2
from datetime import datetime
import numpy as np
import pickle
from time import sleep
import os

scaling_factor = 0.75

width = 1280
height = 720
len_ard_data = 3

record_length = 500

save_net_path = '/home/autonomous-car/Desktop/Autonomous_car_ros2/src/data_store/network_store/rnn_net.pth'


class RNN(nn.Module):
    def __init__(self, Input_size, H1_size, H2_size, H3_size, Out_size):
        super(RNN, self).__init__()

        self.IN = nn.Linear(Input_size, H1_size)

        self.hidden1 = nn.RNN(
            input_size=H1_size,
            hidden_size=H2_size,
            num_layers=3,
            nonlinearity='relu'
        )

        self.hidden2 = nn.Linear(H2_size, H3_size)

        self.out = nn.Linear(H3_size, Out_size)

    def forward(self, x, h_1):

        input_layer = F.relu(self.IN(x))

        '''
        #one of the method to do it
        # Initialize hidden state with zeros
        # (layer_dim, batch_size, hidden_dim)
        h0 = torch.zeros(1, x.size(0), 40).cuda()

        # We need to detach the hidden state to prevent exploding/vanishing gradients
        # This is part of truncated backpropagation through time (BPTT)
        # rnn layer
        h_2, h_n = self.hidden1(input_layer, h0.detach())
        '''

        # rnn layer
        h_2, h_n = self.hidden1(input_layer, h_1)

        h_3 = F.relu(self.hidden2(h_2))
        out_l = self.out(h_3)

        return out_l, h_n


if __name__ == '__main__':

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(torch.cuda.is_available())

    Input_size = int((height*scaling_factor)*(width*scaling_factor*2)*2) + len_ard_data
    H1_size = 60
    H2_size = 500
    H3_size = 500
    Out_size = 3

    rnn = RNN(Input_size, H1_size, H2_size,
              H3_size, Out_size)

    # load_network
    #rnn = torch.load(save_net_path)
    #rnn.eval()

    # just to train again
    # rnn.train()

    # puting the network in gpu
    rnn.cuda()

    # dump information to this variable
    store = np.zeros((record_length, Input_size), dtype=np.float16)

    for i in range(100):

        store = np.load(
            '/home/autonomous-car/Desktop/Autonomous_car_ros2/src/data_store/Data/'+str(i)+'.npy')

        input_a = torch.from_numpy(store)
        input_a = input_a.reshape(record_length,1, 1, Input_size).half()

        target = torch.from_numpy(store[:,Input_size-len_ard_data:Input_size])
        target = target.reshape(record_length,1,1,len_ard_data).half()

        # loss func and optimizer
        criterion = torch.nn.MSELoss().half()
        optimizer = torch.optim.Adam(rnn.parameters(), lr=0.0001)

        # make a loop from here
        for j in range(record_length - 2):
            with autograd.detect_anomaly():

                # making the model ready for half precission
                rnn.half()

                # make the gradiants zero
                rnn.zero_grad()

                #getting input ready
                '''
                #input_a[j] = input_a[j].float()
                input_a[j] = input_a[j].reshape(1, 1, Input_size).half().cuda()
                
                target = torch.ones([1, 5], dtype=torch.float16)
                target = target.reshape(1, 1, Out_size).half().cuda()
                '''

                output, h_n = rnn(input_a[j].cuda(), None)

                '''
                input_a = torch.from_numpy(store[j+1])
                #input_a = input_a.float()
                input_a = input_a.reshape(1, 1, Input_size).half().cuda()
                #target = torch.randn(1, 1, 10).cuda()
                target = torch.ones([1, 5], dtype=torch.float16)
                target = target.reshape(1, 1, Out_size).half().cuda()
                '''

                output, h_n = rnn(input_a[j+1].cuda(), h_n)

                # start training
                optimizer.zero_grad()
                loss = criterion(output, target[j+2].cuda())

                print(str(loss) + ' Frame No.:' + str(j) + '\t Batch:' + str(i))

                loss.backward()

                # optimized doesnt work on well with half(), it makes them nan if i dont convert
                # the model to float() before doing the optimizer step ( weights update )
                rnn.float()

                optimizer.step()

        # saving the training values
        torch.save(rnn, save_net_path)

        print(output)
