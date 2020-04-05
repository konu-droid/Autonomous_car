import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class RNN(nn.Module):
    def __init__(self,Input_size,H1_size,H2_size,H3_size,H4_size,H5_size,Out_size):
        super(RNN, self).__init__()

        self.IN = nn.Linear(Input_size,H1_size)

        self.hidden1 = nn.RNN(         
            input_size=H1_size,
            hidden_size=H2_size,         
            num_layers=3,
            nonlinearity='relu'
        )

        self.hidden2 = nn.Linear(H2_size,H3_size)

        self.hidden3 = nn.Linear(H3_size,H4_size)

        self.out = nn.Linear(H5_size, Out_size)

    def forward(self, x,h_1):
        input_layer = self.IN(x)
        input_layer = F.relu(input_layer)

        #rnn layer
        h_2, h_n = self.hidden1(input_layer, h_1)

        h_3 = self.hidden2(h2)
        h_3 = F.relu(h_3)
        h_4 = self.hidden3(h_3)
        h_4 = F.relu(h_4)
        out_l = self.out(h_4)

        return out_l,h_n


if __name__ == '__main__':
    Input_size = 100
    H1_size = 50
    H2_size = 40
    H3_size = 30
    H4_size = 20
    H5_size = 10
    Out_size = 5

    rnn =RNN(Input_size,H1_size,H2_size,H3_size,H4_size,H5_size,Out_size)
    #print(rnn)

    #load the trained network parameters (edit it for the path and loop)
    # open a file, where you stored the pickled data
    file = open('name_of_the_file', 'rb')

    # dump information to that file
    network_para = pickle.load(file)

    # close the file
    file.close()
    
    #loss func and optimizer
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(rnn.parameters(), lr =0.1)

    #init for rnn hidden
    output,h_n = rnn(input_a,None)

    #make a loop from here
    output1,h = rnn(input_a,h_n)
    print(output)