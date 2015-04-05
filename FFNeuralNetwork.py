import math
import random

class FFNeuralNetwork(object):
    def __init__(self, n_input, n_hidden, n_output, activate_fn=None, outputactivate_fn=None):
        """
        Initializes a Feed Forward neural network.

        Args:
        n_input: # of input nodes
        n_hidden: List of # of hidden nodes for each hidden layer ( [n_hidden1, n_hidden2, ..., n_hiddenk] )
        n_output: List of # of output nodes
        activate: The activation function to use for hidden layer nodes. Sigmoid is default.
        outputactivate: The activation function to use for output layer nodes. Sigmoid is default.
        """
        if not activate_fn:
            self.activate_fn = self.__sigmoid
        if not outputactivate_fn:
            self.outputactivate_fn = self.__sigmoid

        n_hidden_layers = len(n_hidden)
        self.input_layer = []
        self.hidden_layers = []
        self.output_layer = []

        # Create input nodes
        for i in range(n_input):
            node = self.__gen_node("IN #" + str(i))
            self.input_layer.append(node)

        # Create output nodes
        for i in range(n_output):
            node = self.__gen_node("OUT #" + str(i))
            self.output_layer.append(node)

        # Create hidden layer nodes
        for i in range(n_hidden_layers):
            hidden = []

            # Create each node in hidden layer
            for j in range(n_hidden[i]):
                node = self.__gen_node("HIDE #(%d,%d)" % (i, j))
                hidden.append(node)

                # If first hidden layer, inputs are input layer
                if i == 0:
                    node["incoming"] = self.input_layer
                    node["incoming_w"] = [self.__init_weight() for _ in range(n_input)]
                # Otherwise inputs are previous hidden layer
                else:
                    node["incoming"] = self.hidden_layers[i - 1]
                    node["incoming_w"] = [self.__init_weight() for _ in range(n_hidden[i-1])]

                # If last hidden layer, outputs are output layer
                if i == n_hidden_layers - 1:
                    node["outgoing"] = self.output_layer
                    node["outgoing_w"] = [self.__init_weight() for _ in range(n_output)]

            # Link previous layer to this one
            if i == 0:
                prev_layer = self.input_layer
            else:
                prev_layer = self.hidden_layers[i-1]
            for node_prev in prev_layer:
                node_prev["outgoing"] = hidden
                node_prev["outgoing_w"] = [self.__init_weight() for _ in range(n_hidden[i])]

            # Add this hidden layer to list of hidden layers
            self.hidden_layers.append(hidden)

        # Link output nodes to last hidden layer
        for node in self.output_layer:
            node["incoming"] = self.hidden_layers[-1]
            node["incoming_w"] = [self.__init_weight() for _ in range(n_hidden[-1])]


    def __sigmoid(self,x):
        """
        Evaluates the sigmoid activation function for the neural network
        """
        return 1.0/(1.0 + math.exp(-x))


    def __activate(self, x):
        return self.activate_fn(x)

    def __output_activate(self, x):
        return self.outputactivate_fn(x)


    def __init_weight(self):
        """
        Returns a random value for weight initialization of network
        """
        return -1 + 2 * random.random()


    def __gen_node(self, name):
        """
        Generates a new node
            Structure of a node:
                incoming: List of weights of incoming nodes
                outgoing: List of weights of outgoing nodes
                value: The value of this node f(z) = sigmoid(z), z = weighted sum of incoming
        """
        return {"name": name, "incoming": [], "incoming_w": [], "outgoing": [], "outgoing_w": [], "value": 0}

    """
    NOTE TO SELF:
        outgoing and outgoing_w may not actually be necessary at all.
    """

    def send_signal(self, input_values):
        n_inputs = len(self.input_layer)
        n_hidden_layers = len(self.hidden_layers)
        n_outputs = len(self.output_layer)
        assert(n_inputs == len(input_values))

        # Set values of input nodes to raw input values
        for i in range(n_inputs):
            self.input_layer[i]["value"] = input_values[i]

        # Process each hidden layer node
        for i in range(n_hidden_layers):
            for node in self.hidden_layers[i]:
                incoming_values = [node["incoming"][n]["value"] * node["incoming_w"][n] for n in range(len(node["incoming"]))]
                node["value"] = self.__activate(sum(incoming_values))

        # Process each output layer node
        output_values = []
        for node in self.output_layer:
            incoming_values = [node["incoming"][n]["value"] * node["incoming_w"][n] for n in range(len(node["incoming"]))]
            node["value"] = self.__output_activate(sum(incoming_values))
            output_values.append(node["value"])

        return output_values

if __name__ == "__main__":
    NN = FFNeuralNetwork(2,[2],1)
    NN.hidden_layers[0][0]["incoming_w"] = [7,3]
    NN.hidden_layers[0][1]["incoming_w"] = [2,4]
    NN.output_layer[0]["incoming_w"] = [2.5, 3.2]
    print(NN.send_signal([2,3]))
    for n in (NN.input_layer + [l for j in range(len(NN.hidden_layers)) for l in NN.hidden_layers[j]] + NN.output_layer):
        print(n["name"], n["value"])
        print("    ", [d["name"] for d in n["incoming"]] )
        print("    ", [d for d in n["incoming_w"]] )
        print("    ", [d["name"] for d in n["outgoing"]] )
