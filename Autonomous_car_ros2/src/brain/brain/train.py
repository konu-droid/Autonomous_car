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




TRAININGGGGGGGG!!!!!

** First i was using GPU for training but that allowe the maximum of 60 neurons in second layer
   with half precision enabled! but the processing speed was too good like 5 frames per second or even more
** when i make the second layer 300 it take like 45-50 seconds per frame to process since
   9gb of swap has to be loaded after 16gb of normal ram
** when the used 200 neurons for layer two the swap was just 5.5gb -6gb and each frame took 5 seconds. good balance

** Now i have seperated the networks into 4 networks and after every networks finishes one step i take it out of
   GPU memory and put the next net in, this allowed the second layer to be 300 nodes and then train the network on GPU
   vastly increaseing the speed to 6 seconds per frame and swap only used up to 6gb with 16gb ram
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

total_data_size = int((height*scaling_factor) *
                      (width*scaling_factor*2)*2) + len_ard_data

record_length = 500

save_net_path1 = '/home/autonomous-car/Desktop/Autonomous_car_ros2/src/data_store/network_store/rnn1_net.pth'
save_net_path2 = '/home/autonomous-car/Desktop/Autonomous_car_ros2/src/data_store/network_store/rnn2_net.pth'
save_net_path3 = '/home/autonomous-car/Desktop/Autonomous_car_ros2/src/data_store/network_store/rnn3_net.pth'
save_net_path4 = '/home/autonomous-car/Desktop/Autonomous_car_ros2/src/data_store/network_store/rnn4_net.pth'


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

        x = F.relu(self.IN(x))

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
        x, h_n = self.hidden1(x, h_1)

        x = F.relu(self.hidden2(x))
        x = self.out(x)

        return x, h_n


class FF(nn.Module):
    def __init__(self, Input_size, H1_size, H2_size, H3_size, Out_size):
        super(FF, self).__init__()

        self.IN = nn.Linear(Input_size, H1_size)

        self.hidden1 = nn.Linear(H1_size, H2_size)

        self.hidden2 = nn.Linear(H2_size, H3_size)

        self.out = nn.Linear(H3_size, Out_size)

    def forward(self, x):

        x = F.relu(self.IN(x))

        x = F.relu(self.hidden1(x))

        x = F.relu(self.hidden2(x))
        x = self.out(x)

        return x


if __name__ == '__main__':

    #device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(torch.cuda.is_available())

    Input_size = int((height*scaling_factor)*(width*scaling_factor*2))
    H1_size = 300
    H2_size = 500
    H3_size = 500
    Out_size = 3

    final_Input_size = Out_size*3
    final_H1_size = 10
    final_H2_size = 10
    final_H3_size = 10

    rnn = RNN(Input_size, H1_size, H2_size,
              H3_size, Out_size)

    rnn2 = RNN(Input_size, H1_size, H2_size,
               H3_size, Out_size)

    rnn3 = RNN(len_ard_data, final_H1_size, final_H2_size,
               final_H3_size, Out_size)

    final = FF(final_Input_size, final_H1_size,
               final_H2_size, final_H3_size, Out_size)

    # load_network
    #rnn = torch.load(save_net_path)
    # rnn.eval()

    # putting the network in gpu
    rnn.half().cuda()

    # dump information to this variable
    store = np.zeros((record_length, total_data_size), dtype=np.float16)

    for i in range(100):

        store = np.load(
            '/home/autonomous-car/Desktop/Autonomous_car_ros2/src/data_store/Data/'+str(i)+'.npy')

        input_a = torch.from_numpy(store[:, 0:Input_size])
        input_a = input_a.reshape(record_length, 1, 1, Input_size)  # .float()

        input_b = torch.from_numpy(store[:, Input_size:Input_size*2])
        input_b = input_b.reshape(record_length, 1, 1, Input_size)  # .float()

        input_c = torch.from_numpy(store[:, total_data_size-len_ard_data:total_data_size])
        input_c = input_c.reshape(record_length, 1, 1, len_ard_data)  # .float()

        print(input_a.type())

        target = torch.from_numpy(store[:, total_data_size-len_ard_data:total_data_size])
        target = target.reshape(record_length, 1, 1, len_ard_data)  # .float()

        # loss func and optimizer
        criterion = torch.nn.MSELoss().half()
        optimizer = torch.optim.Adam(rnn.parameters(), lr=0.0001)
        optimizer2 = torch.optim.Adam(rnn2.parameters(), lr=0.0001)
        optimizer3 = torch.optim.Adam(rnn3.parameters(), lr=0.0001)
        optimizer4 = torch.optim.Adam(final.parameters(), lr=0.0001)

        # make a loop from here
        for j in range(record_length - 2):
            with autograd.detect_anomaly():

                # making the model ready for half precission
                rnn.half().cuda()

                # getting input ready
                output, h_n = rnn(input_a[j].cuda(), None)

                output, h_n = rnn(input_a[j+1].cuda(), h_n)

                # start training
                optimizer.zero_grad()
                loss = criterion(output, target[j+2].cuda())

                print(str(loss) + ' Frame No.:' +
                      str(j) + '\t Batch:' + str(i))

                loss.backward()

                # optimized doesnt work on well with half(), it makes them nan if i dont convert
                # the model to float() before doing the optimizer step ( weights update )
                rnn.float().cpu()

                optimizer.step()

                torch.cuda.empty_cache()

                '''=================== Second network start=================='''

                # making the model ready for half precission
                rnn2.half().cuda()

                # getting input ready
                output2, h_n = rnn2(input_b[j].cuda(), None)

                output2, h_n = rnn2(input_b[j+1].cuda(), h_n)

                # start training
                optimizer2.zero_grad()
                loss = criterion(output2, target[j+2].cuda())

                print(str(loss) + ' Frame No.:' +
                      str(j) + '\t Batch:' + str(i))

                loss.backward()

                # optimized doesnt work on well with half(), it makes them nan if i dont convert
                # the model to float() before doing the optimizer step ( weights update )
                rnn2.float().cpu()

                optimizer2.step()

                torch.cuda.empty_cache()

                '''=================== Third network start=================='''

                # making the model ready for half precission
                rnn3.half().cuda()

                # getting input ready
                output3, h_n = rnn3(input_c[j].cuda(), None)

                output3, h_n = rnn3(input_c[j+1].cuda(), h_n)

                # start training
                optimizer3.zero_grad()
                loss = criterion(output3, target[j+2].cuda())

                print(str(loss) + ' Frame No.:' +
                      str(j) + '\t Batch:' + str(i))

                loss.backward()

                # optimized doesnt work on well with half(), it makes them nan if i dont convert
                # the model to float() before doing the optimizer step ( weights update )
                rnn3.float()

                optimizer3.step()

                torch.cuda.empty_cache()

                '''=================== Fourth network start=================='''

                # making the model ready for half precission
                final.half().cuda()

                #detach all the outputs till now
                #this is so that now the loss.backward() will not track back the other 3 networks
                output = output.detach()
                output2 = output2.detach()
                output3 = output3.detach()

                #input
                final_input = torch.cat((output,output2,output3),1)
                final_input = final_input.reshape(1, 1, final_Input_size)

                # getting input ready
                output4= final(final_input.cuda())

                # start training
                optimizer4.zero_grad()
                loss = criterion(output4, target[j+2].cuda())

                print(str(loss) + ' Frame No.:' +
                      str(j) + '\t Batch:' + str(i))

                loss.backward()

                # optimized doesnt work on well with half(), it makes them nan if i dont convert
                # the model to float() before doing the optimizer step ( weights update )
                final.float()

                optimizer4.step()

                torch.cuda.empty_cache()
                  

        # saving the training values
        torch.save(rnn, save_net_path1)
        torch.save(rnn2, save_net_path2)
        torch.save(rnn3, save_net_path3)
        torch.save(final, save_net_path4)

        print(output)
