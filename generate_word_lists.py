
if __name__ == "__main__":
    word_list = []
    with open('dictionary.txt', 'r') as f:
        for line in f:
            word_list.append(line.strip())        
    f.close()
    
    master_list = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
    
    for i in range(4, 16):
        for word in word_list:
            if "'" not in word and len(word) == i:
                master_list[i-4].append(word)
             
    print(master_list)
    master_list = str(master_list)
    
    
    with open('word_lists.py', 'w') as f:
        f.write("master_list = ")
        f.write(master_list)
    f.close()
    