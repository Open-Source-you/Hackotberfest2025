# The code implements a rock, paper, scissors player using a machine learning approach. It uses a Long Short-Term Memory(LSTM) neural network to predict the opponent's next move based on their history of moves. The main components of the code are:
# Data preparation functions
# Model building and training functions
# Move prediction and counter-move selection
# The main player function that combines all these elements

import random

import keras
import numpy as np
import tensorflow as tf
from keras import layers, optimizers

tf.keras.utils.disable_interactive_logging()

model = None
UPDATE_FREQUENCY = 30  # Frequency of Updating the model with new data
SEQUENCE_LENGTH = 20  # Number of moves to consider for prediction
TRAINING_ITERATIONS = 0

is_quincy = False
is_kris = False
is_mrugesh = False
is_abbey = False

my_moves = []

assert (
    UPDATE_FREQUENCY > SEQUENCE_LENGTH
), f"UPDATE_FREQUENCY ({UPDATE_FREQUENCY}) must be greater than SEQUENCE_LENGTH ({SEQUENCE_LENGTH})"


def calculate_move_frequency(history, window_size=50):
    """
    calculate the frequency of each move in the recent history
    """
    recent_history = history[-window_size:]
    total_moves = len(recent_history)
    frequency = {
        "R": recent_history.count("R") / total_moves,
        "P": recent_history.count("P") / total_moves,
        "S": recent_history.count("S") / total_moves,
    }
    return frequency


def get_previous_results(history, window_size=10):
    """
    track the results of previous games
    """
    results = []
    for i in range(1, min(window_size, len(history))):
        prev_move = history[-i - 1]
        current_move = history[-i]
        if prev_move == current_move:
            results.append(0)  # Tie
        elif (
            (prev_move == "R" and current_move == "P")
            or (prev_move == "P" and current_move == "S")
            or (prev_move == "S" and current_move == "R")
        ):
            results.append(1)  # Win
        else:
            results.append(-1)  # Loss
    return results


def prepare_data(history, sequence_length=SEQUENCE_LENGTH):
    """
    Prepares the data for training the RPS model by converting the move history into a sequence of integers and adding additional features.

    Args:
        history (list): The history of moves played.
        sequence_length (int): The number of previous moves to consider for prediction.

    Returns:
        Tuple[np.ndarray, np.ndarray]: The input sequences (X) and the corresponding target moves (y).
    """
    X, y = [], []
    if len(history) > sequence_length:
        for i in range(len(history) - sequence_length):
            sequence = [move_to_int(m) for m in history[i : i + sequence_length] if m]
            if len(sequence) == sequence_length:
                # Add move frequency
                freq = calculate_move_frequency(history[: i + sequence_length])
                sequence.extend([freq["R"], freq["P"], freq["S"]])

                # Add previous results
                results = get_previous_results(history[: i + sequence_length])
                sequence.extend(results)

                X.append(sequence)
                y.append(move_to_int(history[i + sequence_length]))
    return np.array(X), np.array(y)


def move_to_int(move):
    valid_moves = {"R": 0, "P": 1, "S": 2}
    if move in valid_moves:
        return valid_moves[move]
    else:
        raise ValueError(f"Invalid move_to_int {move}")


def int_to_move(int_move):
    if 0 <= int_move <= 2:
        return {0: "R", 1: "P", 2: "S"}[int_move]
    else:
        raise ValueError(f"Invalid int_to_move {int_move}")


# This approach uses a Sequential model with an LSTM layer to learn patterns in the opponent's moves.
# It trains on the entire history each time, which might be computationally expensive for long games.
# For better performance, you could train the model periodically or use online learning techniques.


def build_model(learning_rate=0.001):
    """
    Builds and compiles a Sequential model with LSTM layers for predicting RPS moves.
    The LSTM layer is followed by a dense layer with ReLU activation, which can help capture more complex patterns.

    Args:
        sequence_length (int): The number of previous moves to consider for prediction.

    Returns:
        keras.models.Sequential: The compiled model.
    """
    input_shape = (
        SEQUENCE_LENGTH + 3 + 10
    )  # Sequence + 3 frequencies + 10 previous results
    model = keras.Sequential(
        [
            layers.Input(shape=(input_shape, 1)),
            layers.LSTM(32),
            layers.Dense(16, activation="relu"),
            layers.Dense(3, activation="softmax"),
        ]
    )
    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def get_dynamic_learning_rate(initial_rate=0, decay_factor=0, min_rate=0):
    # initial_rate=0.001, decay_factor=0.95, min_rate=0.0001
    """
    Dynamic Learning Rate
    The get_dynamic_learning_rate function implements a decaying learning rate strategy
    This can help the model converge more effectively as training progresses.
    """
    global TRAINING_ITERATIONS
    learning_rate = max(initial_rate * (decay_factor**TRAINING_ITERATIONS), min_rate)
    TRAINING_ITERATIONS += 1
    return learning_rate


@tf.function(
    input_signature=[
        tf.TensorSpec(shape=(1, SEQUENCE_LENGTH, 1), dtype=tf.float32),
        tf.TensorSpec(shape=(1,), dtype=tf.int32),
    ]
)
def train_step(x, y):
    with tf.GradientTape() as tape:
        logits = model(x, training=True)
        loss_value = tf.keras.losses.sparse_categorical_crossentropy(y, logits)
    grads = tape.gradient(loss_value, model.trainable_weights)
    model.optimizer.apply_gradients(zip(grads, model.trainable_weights))
    return loss_value


def train_model(history):
    """
    Trains the model on the provided game history.

    Args:
        history (list): A list of the opponent's previous moves, represented as strings ('R', 'P', 'S').

    Returns:
        keras.models.Sequential: The trained model.
    """
    X, y = prepare_data(history)
    if len(X) > 0 and len(y) > 0:
        learning_rate = get_dynamic_learning_rate()
        model = build_model(learning_rate)
        model.fit(X, y, epochs=20, verbose=0)
        return model
    return None


def check_if_quincy(opponent_history):
    """
    Checks if the opponent's move history matches the known pattern of Quincy's play.

    Args:
        opponent_history (list): A list of the opponent's previous moves, represented as strings ('R', 'P', 'S').

    Returns:
        bool: True if the opponent's move history matches Quincy's pattern, False otherwise.
    """
    if len(opponent_history) >= 5:
        quincy_pattern = ["R", "R", "P", "P", "S"]
        start_index = (len(opponent_history) + 1) % 5
        expected_pattern = quincy_pattern[start_index:] + quincy_pattern[:start_index]
        last_five = opponent_history[-5:]

        # print(
        #     f"Checking pattern {expected_pattern} starting at index {start_index}")
        # print(f"Last five moves: {last_five}")
        # print(f"Expected pattern: {expected_pattern}")

        if all(a == b for a, b in zip(last_five, expected_pattern)):
            print(f"Playing Against Quincy")
            return True
        else:
            print(f"Expected pattern {expected_pattern} not equal to {last_five}")
            print(f"Not playing against Quincy")
            return False
    return True


def quincy_counter(round_number):
    quincy_sequence = ["R", "R", "P", "P", "S"]
    predicted_move = quincy_sequence[(round_number + 1) % 5]
    print(f"Quincy prediction {predicted_move}")
    my_counter = counter_move(predicted_move)
    print(f"I played {my_counter}")
    return my_counter


def check_if_mrugesh(opponent_history, my_moves):
    if len(my_moves) >= 10:
        # last_ten = my_moves[-10:]
        last_ten = my_moves[-11:-1]
        most_frequent = max(set(last_ten), key=last_ten.count)
        if most_frequent == "":
            most_frequent = "S"
        ideal_response = {"P": "S", "R": "P", "S": "R"}
        expected_move = ideal_response[most_frequent]
        if opponent_history[-1] == expected_move:
            print("Playing Against Mrugesh")
            return True
        else:
            print("Not playing against Mrugesh")
            print(f"Expected move {expected_move} but got {opponent_history[-1]}")
            return False
    return True


def mrugesh_counter(my_moves):
    last_ten = my_moves[-10:]
    most_frequent = max(set(last_ten), key=last_ten.count)
    predicted_move = counter_move(most_frequent)
    print(f"Mrugesh prediction {predicted_move}")
    my_counter = counter_move(predicted_move)
    print(f"I played {my_counter}")
    return my_counter


def check_if_kris(opponent_history, my_moves):
    if len(opponent_history) >= 3 and len(my_moves) >= 2:
        prev_my_play = my_moves[-2]
        # print(f"prev_my_play {prev_my_play}")
        kris_planned_move = counter_move(prev_my_play)
        # print(f"kris_planned_move {kris_planned_move} opponent_history[-1] {opponent_history[-1]}")
        if opponent_history[-1] == kris_planned_move:
            print("Playing Against Kris")
            return True
        else:
            print("Not playing against Kris")
            return False
    return True


def kris_counter(prev_play, my_moves):
    predicted_move = counter_move(my_moves[-1])
    # print(f"Kris prediction {predicted_move}")
    my_counter = counter_move(predicted_move)
    # print(f"I played {my_counter}")
    return my_counter


def check_if_abbey(opponent_history, my_moves, confidence_threshold=0.6):
    if len(my_moves) < 10:  # Increased minimum history for better accuracy
        return True

    play_order = {
        "RR": 0,
        "RP": 0,
        "RS": 0,
        "PR": 0,
        "PP": 0,
        "PS": 0,
        "SR": 0,
        "SP": 0,
        "SS": 0,
    }

    for i in range(len(my_moves) - 2):
        key = my_moves[i] + my_moves[i + 1]
        if key in play_order:
            play_order[key] += 1

    correct_predictions = 0
    total_predictions = 0

    for i in range(2, len(my_moves)):
        last_two = "".join(my_moves[i - 2 : i])
        potential_plays = [last_two[1] + "R", last_two[1] + "P", last_two[1] + "S"]
        sub_order = {k: play_order[k] for k in potential_plays if k in play_order}

        if sub_order:
            prediction = max(sub_order, key=sub_order.get)[-1:]
            expected_move = counter_move(prediction)
            if opponent_history[i] == expected_move:
                correct_predictions += 1
            total_predictions += 1

    if total_predictions > 0:
        accuracy = correct_predictions / total_predictions
        if accuracy >= confidence_threshold:
            print(f"Playing Against Abbey (Confidence: {accuracy:.2f})")
            return True
        else:
            print(f"Not playing against Abbey (Confidence: {accuracy:.2f})")
            return False
    else:
        return True  # Continue checking if not enough predictions


def abbey_counter(my_moves):
    play_order = {
        "RR": 0,
        "RP": 0,
        "RS": 0,
        "PR": 0,
        "PP": 0,
        "PS": 0,
        "SR": 0,
        "SP": 0,
        "SS": 0,
    }

    for i in range(len(my_moves) - 2):
        key = my_moves[i] + my_moves[i + 1]
        if key in play_order:
            play_order[key] += 1

    last_two = "".join(my_moves[-2:])
    potential_plays = [last_two[1] + "R", last_two[1] + "P", last_two[1] + "S"]

    sub_order = {k: play_order[k] for k in potential_plays if k in play_order}
    if not sub_order:
        return random.choice(["R", "P", "S"])

    prediction = max(sub_order, key=sub_order.get)[-1:]
    abbey_move = counter_move(prediction)

    # Implement a mixed strategy
    if random.random() < 0.8:  # 80% of the time, use the counter strategy
        my_counter = counter_move(abbey_move)
    else:  # 20% of the time, play randomly to avoid being too predictable
        my_counter = random.choice(["R", "P", "S"])

    print(f"Abbey prediction {abbey_move}")
    print(f"I played {my_counter}")
    return my_counter


def counter_move(move):
    return {"R": "P", "P": "S", "S": "R"}[move]


def track_my_moves(move, my_moves=[]) -> list:
    my_moves.append(move)
    return my_moves


# Initialize the model at the start of the game and update it periodically

# Implement online learning to update the model with each new move
# This code segment does the following:
# 1. It checks if we have enough history(more than 10 moves).
# 2. If so, it prepares a single training example:
# - X is the sequence of the last 10 moves(excluding the most recent one).
# - y is the most recent move(which we're trying to predict).
# 3. It then calls model.train_on_batch(X, y), which updates the model's weights based on this single example.
# This approach is called online learning because it updates the model incrementally with each new piece of data,
# rather than training on the entire dataset at once. This allows the model to adapt quickly to changes in the opponent's strategy
# while being computationally efficient.


def player(prev_play, opponent_history=[]):
    """
    Determines the next move based on the opponent's history and model predictions.
    This function implements both incremental training and periodic batch retraining.

    Args:
        prev_play (str): The opponent's previous move.
        opponent_history (list): A list of the opponent's moves so far.

    Returns:
        str: The next move to play ('R', 'P', or 'S').
    """
    global model, my_moves, is_quincy, is_mrugesh, is_kris, is_abbey

    my_next_move = None

    if not prev_play:
        opponent_history.clear()
        my_moves = []
        # Build the model at start of the game and update it periodically
        model = build_model()
        is_quincy = is_mrugesh = is_kris = is_abbey = True
    else:
        opponent_history.append(prev_play)
        if len(opponent_history) > SEQUENCE_LENGTH:
            X, y = prepare_data(opponent_history[-SEQUENCE_LENGTH:])
            if len(X) > 0 and len(y) > 0:
                # Incremental update for online learning
                model.train_on_batch(X, y)

    if len(opponent_history) <= 2:
        # Random outputs until we have enough history
        my_next_move = random.choice(["R", "P", "S"])
        my_moves = track_my_moves(my_next_move)
        return my_next_move

    # Need to keep checking who the opponent is
    if is_kris:
        if check_if_kris(opponent_history, my_moves):
            my_next_move = kris_counter(prev_play, my_moves)
        else:
            is_kris = False

    if not is_kris and is_quincy:
        if check_if_quincy(opponent_history):
            my_next_move = quincy_counter(len(opponent_history))
        else:
            is_quincy = False

    if not is_kris and not is_quincy and is_mrugesh:
        if check_if_mrugesh(opponent_history, my_moves):
            my_next_move = mrugesh_counter(my_moves)
        else:
            is_mrugesh = False

    if not is_kris and not is_quincy and not is_mrugesh and is_abbey:
        # if check_if_abbey(opponent_history, my_moves):
        #     my_next_move = abbey_counter(my_moves)
        # else:
        #     is_abbey = False
        my_next_move = abbey_counter(my_moves)

    if not is_kris and not is_quincy and not is_abbey and not is_mrugesh:
        # Periodic batch retraining
        if len(opponent_history) % UPDATE_FREQUENCY == 0:
            # print(f"Retraining model with {len(opponent_history)} moves...")
            try:
                learning_rate = get_dynamic_learning_rate()
                new_model = train_model(opponent_history)
                if new_model is not None:
                    model = new_model
                # print(f"Current learning rate: {learning_rate}")
            except Exception as e:
                print(f"Error during model training: {e}")

        try:
            sequence = [move_to_int(m) for m in opponent_history[-SEQUENCE_LENGTH:]]
            freq = calculate_move_frequency(opponent_history)
            sequence.extend([freq["R"], freq["P"], freq["S"]])
            results = get_previous_results(opponent_history)
            sequence.extend(results)

            X = np.array([sequence])
            prediction = model.predict(X)
            predicted_move = int_to_move(np.argmax(prediction[0]))
            my_next_move = counter_move(predicted_move)
        except Exception as e:
            print(f"Error during prediction: {e}")
            my_next_move = random.choice(["R", "P", "S"])
    my_moves = track_my_moves(my_next_move)
    return my_next_move
