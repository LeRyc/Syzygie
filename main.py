#!/usr/bin/env python

__author__ = 'rychly'

"""ai_hw_01.py, Leonard Rychly, 2015-11-25
This program is an assignment within the course 'Artificial Intelligence' of TUM
"""

import sys


# preprocessing data ***************************************************************************************************


def preprocessData(data, root):

    # delete new line character of each word
    for i in range(len(data)-1):
        data[i] = data[i][:-1]
    if '\n' in data[len(data)-1]:   # check if last line is blank (if second last ends with \n)
        del data[len(data)-1]

    # delete all words with less than two characters
    removelist = []
    for i in range(len(data)):
        if len(data[i]) < 2:
            removelist.append(data[i])
    for i in range(len(removelist)):
        data.remove(removelist[i])

    # create list with all possible start/end combination of letters [aa,ab,ac,...,zy,zz]
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    alphabet_pair_list = []
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            pair = alphabet[i]+alphabet[j]
            alphabet_pair_list.append(pair)

    # sort all words depending on their two starting and two end letters in lists (=> create all possible children)
    children_sorted_front = [[]]
    children_sorted_back = [[]]
    for i in range(len(alphabet_pair_list)):
        children_sorted_front.append([])
        children_sorted_back.append([])

    for i in range(len(data)):
        front = data[i][:2]
        front_index = alphabet_pair_list.index(front)
        children_sorted_front[front_index].append(data[i])

        back = data[i][-2:]
        back_index = alphabet_pair_list.index(back)
        children_sorted_back[back_index].append(data[i])

    return [data, children_sorted_front, children_sorted_back]


# get Children from list ***********************************************************************************************


def getChildrenList(root, word, children_sorted_front, children_sorted_back , already_checked_index):
    # already_checked_index: [0]=>front, [1]=>back
    children = []

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    front = word[:2]
    front_index_1 = alphabet.index(front[0])
    front_index_2 = alphabet.index(front[1])
    front_index = front_index_1*26+front_index_2
    if front_index not in already_checked_index[0]:
        children.extend(children_sorted_back[front_index])    # get matching children to front letters
        already_checked_index[0].append(front_index)

    back = word[-2:]
    back_index_1 = alphabet.index(back[0])
    back_index_2 = alphabet.index(back[1])
    back_index = back_index_1*26+back_index_2
    if back_index not in already_checked_index[1]:
        children.extend(children_sorted_front[back_index])    # get matching children to rear letters
        already_checked_index[1].append(back_index)

    return children, already_checked_index


# check if done ********************************************************************************************************


def checkIfDone(endword, children):
    if endword in children:
        return True
    else:
        return False


# build node list ******************************************************************************************************


def buildNodelist(start_word, end_word, children_sorted_front, children_sorted_back):
    nodelist = []

    # create root
    word = start_word
    already_checked_index = [[], []]
    children, already_checked_index = getChildrenList(start_word, word, children_sorted_front,
                                                      children_sorted_back, already_checked_index)    # search children
    node = [word, children, []]
    nodelist.append(node)

    #children to nodes in list (don't get new children of these children)
    for i in range(len(children)):
        new_node = [children[i], [], word]    # [word, children, parent]
        nodelist.append(new_node)

    if checkIfDone(end_word, children) is True:    # check if done
        return [node[0], 0]
    else:

        counter = 1    # 0 was root and has been checked => continue with 1
        # found_word = False

        while True:
            # check next word in list
            word = nodelist[counter][0]
            # print('counter: ', counter, ' => word: ', nodelist[counter][0])
            children, already_checked_index = getChildrenList(start_word, word, children_sorted_front,
                                                              children_sorted_back, already_checked_index)
            nodelist[counter][1] = children    # add children to node
            parent = word    # word becomes parent for his children

            # children to nodelist (without checking new children)
            for i in range(len(children)):
                node = [children[i], [], parent]
                nodelist.append(node)

            # check children if done
            if checkIfDone(end_word, children) is True:
                # found_word = True
                return [nodelist, counter]

            counter += 1


# get path *************************************************************************************************************
# search tree backwards and create path from root to final word

def getPath(final_node_index, node_list, root_word):
    path = []

    # list only of words from node list
    word_list = []
    for i in range(len(node_list)):
        word_list.append(node_list[i][0])

    # first path_list entry: parent of final word
    word_index = final_node_index   # get index of word
    word = node_list[word_index][0]    # get word
    parent = node_list[word_index][2]    # get parent of word

    node = [word_index, word, parent]
    path.append(node)

    while parent is not root_word:
        word = parent
        word_index = word_list.index(word)
        parent = node_list[word_index][2]

        node = [word_index, word, parent]
        path.append(node)

    return path


# main *****************************************************************************************************************


def main():

    name_check = input('=> Please make sure that the word file is in the same folder as the program file.\n'
                       'Is the word file named: wordsEn.txt? (y/n) :')
    if name_check == 'n':
        file_name = input('Now enter the full file name containing the word list (e.g.: words.txt)')
    elif name_check == 'y':
        file_name = 'wordsEn.txt'
    else:
        print('Error: wrong input!')
        sys.exit()

    rootword = input("Enter starting word: ")
    finalword = input("Enter final word: ")

    # read datafile into list
    datafile = open(file_name)
    data = datafile.readlines()
    datafile.close()

    # preprocess data
    print('Preprocessing the data...')
    [data, children_list_front, children_list_back] = preprocessData(data, rootword)

    # check if datafile consists the requested words
    if rootword not in data:
        print("The first word is not in the list")
        if finalword not in data:
            print("The last word is not in the list")
            sys.exit()  # exit program if words are not in datafile
        sys.exit()  # exit program if words are not in datafile

    # delete root word from data
    data.remove(rootword)

    # start building node list
    print('Building search tree...')
    [nodelist, final_node_number] = buildNodelist(rootword, finalword, children_list_front, children_list_back)
    print('Generating path...')
    path = getPath(final_node_number, nodelist, rootword)
    print('*** Path: ***')
    print(rootword)
    for i in reversed(range(len(path))):
        print(path[i][1])
    print(finalword)
    print('*************')


if __name__ == "__main__":   # if someone executes this program as a main program: execute main()
    main()

