import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_Qnet(nn.Module):
    #feet forward neural network with input, hidden, and output layer
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn. Linear(hidden_size, output_size)

    #actuation function and rectifying linear unit
    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name = "Model.pth"):
        model_folder_path = './Model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, learning_rate, gamma):
        self.learning_rate = learning_rate
        self.model = model
        self.gamma = gamma
        self.optimize = optim.Adam(model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def trainer(self, state, action, reward, new_state, game_over):
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        new_state = torch.tensor(new_state, dtype=torch.float)

        if len(state.shape) == 1:
            #if true then only 1 dimension
            state = torch.unsqueeze(state, 0) # adds one dimension
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            new_state = torch.unsqueeze(new_state, 0)
            game_over = (game_over, )

        # bellman equation; Predict Q vals of current state
        pred = self.model(state)
        #apply reward + gamma * max(next_pred_Q_val); only apply if not applied previously
        tar = pred.clone()
        for i in range(len(game_over)):
            new = reward[i]
            if not game_over[i]:
                new = reward[i] + self.gamma * torch.max(self.model(new_state[i]))
            tar[i][torch.argmax(action[i]).item()] = new
        self.optimize.zero_grad()
        loss = self.criterion(tar, pred)
        loss.backward() #backpropigation
        self.optimize.step()








