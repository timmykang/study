def group_by_n(s, n=2):
    # takes a list or tuple and chunks it up into pairs or other n
    # e.g. (1,2,3,4,5,6) -> ((1,2),(3,4),(5,6))
    return [s[i:i + n] for i in range(0, len(s), n)]

def msg_internal_validity(msg, identity):
    # test zuccoin transaction message validity
    msg_list = msg.split(' ')
    return msg_list[0] == identity and \
        msg_list[1] == 'sent' and \
        float(msg_list[2]) < 500 and \
        msg_list[3] == 'zuccoins' and \
        msg_list[4] == 'to' and \
        len(msg_list[5]) == 64 and \
        len(msg_list) == 6


