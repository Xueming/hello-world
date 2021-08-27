def target_ports():
    f = open("arguments/target_ports.txt", "r")
    lines = f.readlines()
    for i in range(0, len(lines)):
        lines[i] = lines[i].strip()
    return lines


def login_account():
    f = open("arguments/login_account.txt", "r")
    line = f.readline()
    return line.split('/')

