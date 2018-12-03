from csv import reader
from math import log
from TreeNode import TreeNode


def data_pre_process(data_set, continuous_variable_indices, titles):
    for index in continuous_variable_indices:
        value_list = []
        for row in data_set:
            value_list.append(row[index])

        value_list = list(map(int, value_list))

        max_val = max(value_list)
        min_val = min(value_list)

        midpoint = (max_val + min_val) // 2
        left_midpoint = (min_val + midpoint) // 2
        right_midpoint = (max_val + midpoint) // 2

        for row in data_set:
            value = int(row[index])
            if value < left_midpoint:
                row[index] = str(titles[index]) + " < " + str(left_midpoint)
            elif left_midpoint <= value < midpoint:
                row[index] = str(titles[index]) + " between " + str(left_midpoint) + " and " + str(midpoint)
            elif midpoint <= value < right_midpoint:
                row[index] = str(titles[index]) + " between " + str(midpoint) + " and " + str(right_midpoint)
            else:
                row[index] = str(titles[index]) + " > " + str(right_midpoint)


def unique_values(data_set, column_index):
    all_responses = []
    for row in data_set:
        all_responses.append(row[column_index])

    unique_responses = list(set(all_responses))

    return unique_responses, all_responses


def response_extraction(data_set, column_index, response, outcomes):
    extracted_set = []
    extracted_outcomes = []

    for i in range(0, len(data_set)):
        if response == data_set[i][column_index]:
            extracted_set.append(data_set[i])
            extracted_outcomes.append(outcomes[i])

    return extracted_set, extracted_outcomes


def outcome_entropy(outcomes):
    unique_outcomes = list(set(outcomes))

    entropy_value = 0

    for outcome in unique_outcomes:
        p_value = outcomes.count(outcome) / float(len(outcomes))
        entropy_value += p_value * log(p_value, 2)

    return -entropy_value


def conditional_entropy(data_set, outcomes, column_index):
    unique_responses, all_responses = unique_values(data_set, column_index)
    unique_outcomes = list(set(outcomes))

    conditional_entropy_value = 0

    for response in unique_responses:
        entropy_value = 0

        response_probability = all_responses.count(response) / float(len(all_responses))
        extracted_set, extracted_outcomes = response_extraction(data_set, column_index, response, outcomes)

        for outcome in unique_outcomes:
            p_value = extracted_outcomes.count(outcome) / float(len(extracted_outcomes))
            if p_value > 0.0:
                entropy_value += p_value * log(p_value, 2)
        entropy_value = -entropy_value

        conditional_entropy_value += response_probability * entropy_value

    return conditional_entropy_value


def information_gain_max(number_of_features, outcomes, data_set):
    maximum = [-1, None]

    information_gain_list = []

    for i in range(0, number_of_features):
        information_gain = outcome_entropy(outcomes) - conditional_entropy(data_set, outcomes, i)
        information_gain_list.append([information_gain, i])

    for row in information_gain_list:
        if row[0] > maximum[0]:
            maximum = row

    return maximum


def row_check(data_set, column_index, value):
    boolean = False

    for row in data_set:
        if value in row[column_index]:
            boolean = True

    return boolean


def print_tree(tree_node, depth=0):
    if not tree_node.children:
        print(depth*"\t" + "Decision: " + str(tree_node.decision))
    else:
        print(depth*"\t" + "Split on " + str(tree_node.split_title))
        for child in tree_node.children:
            child, tree_branch = child
            print(depth*"\t" + "If " + str(tree_branch))
            print_tree(child, depth + 1)


def decision_tree(training_set, outcomes, titles):
    number_of_features = len(titles) - 1

    maximum = information_gain_max(number_of_features, outcomes, training_set)
    information_gain, column_index = maximum

    possible_answers = unique_values(training_set, column_index)
    possible_answers = possible_answers[0]

    parent_node = TreeNode(parent=None, answer_list=possible_answers, split_title=titles[column_index],
                           split_index=column_index)

    queue = []
    data_set = training_set
    queue.append([data_set, outcomes, column_index, parent_node])

    while len(queue) != 0:
        data_set, outcomes, column_index, node = queue.pop(0)

        possible_answers = unique_values(training_set, column_index)
        possible_answers = possible_answers[0]

        for answer in possible_answers:
            if row_check(data_set, column_index, answer):
                extracted_set, extracted_outcomes = response_extraction(data_set, column_index, answer, outcomes)
                maximum = information_gain_max(number_of_features, extracted_outcomes, extracted_set)
                extracted_information_gain, extracted_index = maximum
                extracted_possible_answers = unique_values(extracted_set, extracted_index)
                extracted_possible_answers = extracted_possible_answers[0]

                if extracted_information_gain == 0:
                    new_node = TreeNode(parent=node, answer_list=extracted_possible_answers, tree_branch=answer,
                                        decision=extracted_outcomes[0], children=[])
                    node.children.append([new_node, answer])
                else:
                    new_node = TreeNode(parent=node, answer_list=extracted_possible_answers, tree_branch=answer,
                                        children=[], split_title=titles[extracted_index], split_index=extracted_index)
                    queue.append([extracted_set, extracted_outcomes, extracted_index, new_node])
                    node.children.append([new_node, answer])
            else:
                new_node = TreeNode(parent=node, answer_list=possible_answers, tree_branch=answer,
                                    decision="unknown", children=[])
                node.children.append([new_node, answer])

    return parent_node


def predict(tree, data_set):
    predictions = []
    parent_tree = tree

    for row in data_set:
        prediction = None
        tree = parent_tree
        while not prediction:
            if tree.decision is not None:
                prediction = tree.decision
                predictions.append(prediction)
            else:
                answer = row[tree.split_index]
                child_tree = tree.find_child(answer)
                tree = child_tree[0]

    return predictions


def confusion_matrix(predictions, outcomes):
    correct = incorrect = true_neg = true_pos = false_neg = false_pos = 0

    for i in range(0, len(predictions)):
        if predictions[i] == outcomes[i]:
            correct = correct + 1
            if outcomes[i] == "no":
                true_neg = true_neg + 1
            else:
                true_pos = true_pos + 1
        else:
            incorrect = incorrect + 1
            if outcomes[i] == "no":
                false_pos = false_pos + 1
            else:
                false_neg = false_neg + 1

    print("\tConfusion Matrix")
    print("\tY\tN")
    print("Y\t"+str(true_pos)+"\t"+str(false_neg))
    print("N\t"+str(false_pos)+"\t"+str(true_neg))
    print("Percent Correct: " + str((correct / len(predictions) * 100)) + "%")


if __name__ == "__main__":
    data_matrix = list(reader(open('credit.csv')))

    titles = data_matrix.pop(0)
    outcomes = []

    for row in data_matrix:
        outcomes.append(row.pop())

    data_pre_process(data_matrix, [1, 4, 9], titles)

    training_set = data_matrix[:800]
    testing_set = data_matrix[800:]
    training_outcomes = outcomes[:800]
    testing_outcomes = outcomes[800:]

    tree = decision_tree(training_set, training_outcomes, titles)
    print_tree(tree)
    print("")

    testing_predictions = predict(tree, testing_set)

    confusion_matrix(testing_predictions, testing_outcomes)
