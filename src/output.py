import os

def print_to_txt(nodes, model, number):

    output_folder = os.path.join(os.getcwd(), 'Solution')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filename = "output-"

    output_path = os.path.join(output_folder, f'{filename}{number}.txt')
    with open(output_path, 'w') as file:
        if model is None:
            file.write("No model")
            print("No model")
            return
        j = 0
        def Index(i): return (i // 4) // len(nodes[0])

        """ 
            0 0 0 0 0 | 0 2 0 1 0 | 0 0 0 0 0 | 0 1 0 0 0 | 0 0 0 0 0 
        """ 

        for i in range(0, len(model), 4):
            if nodes[Index(i)][j].weight != 0:
                file.write(f'{nodes[Index(i)][j].weight} ')
                print(f'{nodes[Index(i)][j].weight} ', end=' ')
            else:
                if Index(i) == 0 or (Index(i) == len(nodes) - 1) or j == 0 or (j == len(nodes[0]) - 1):
                    pass
                else:
                    chunk = model[i:i + 4]

                    to_write = '0 '
                    for c in chunk:
                        if c > 0:
                            # print corresponding bridge symbol from {v1, v2, h1, h2}
                            # 104: h, 118: v 
                            to_write = chr(104 + ((c - i) // 3) *
                                        14) + f"{((c + 1) % 2) + 1}"
                            
                            if to_write == "h1": to_write = "- " 
                            elif to_write == "h2": to_write = "= "
                            elif to_write == "v1": to_write = "| "
                            elif to_write == "v2": to_write = "$ " 
                    file.write(to_write)
                    print(to_write, end=' ')

            j += 1
            if (((i // 4) + 1) % len(nodes[0])) == 0:
                file.write('\n')
                print('\n')
                j = 0
            else:
                file.write('  ')
                print('  ', end=' ') 