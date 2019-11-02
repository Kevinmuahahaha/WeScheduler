#!/usr/bin/python3

def parse_file():
    # returns target user and massages to send to
    # Format:
    #   ['time','user','msg']
    send_content = []

    try:
        msg_list = open('./msg_list.txt',"r")
    except:
        print("[error] Config Not Found")
        return send_content

    inside_tag = False
    user_found = False
    msg_found = False

    tmp_name = ""
    tmp_time = ""
    tmp_msg  = ""
    info_count = 0 # when its 3, its done, append'em to [send_content]

    for line in msg_list.readlines():

        if len(line) >= 1:
            #### Find Tag
            if not inside_tag and line[0] == '[' and line[len(line)-2] == ']':
                inside_tag = True # Start Looking For User and Line
                tmp_name = ""
                tmp_time = ""
                tmp_msg  = ""
                info_count = 0
                continue

            if info_count is 3 and inside_tag:
                inside_tag = False
                info_count = 0
                send_content.append( tmp_time )
                send_content.append( tmp_name )
                send_content.append( tmp_msg )

            if inside_tag:
                line_content = line.split(':')
                identifier = line_content[0]
                try:
                    if identifier == 'NAME':
                        conlon_index = 0
                        for char in line:
                            if char == ':':
                                break
                            else:
                                conlon_index += 1
                        for char in line[conlon_index+1: len(line)]:
                            tmp_name += char
                        info_count += 1

                    if identifier == 'TIME':
                        conlon_index = 0
                        for char in line:
                            if char == ':':
                                break
                            else:
                                conlon_index += 1

                        tmp_time_unstripped = ""
                        for char in line[conlon_index+1: len(line)]:
                            tmp_time_unstripped += char

                        tmp_time_unstripped = tmp_time_unstripped.strip()
                        tmp_time = tmp_time_unstripped.split(' ')[0].strip() + ' ' + tmp_time_unstripped.split(' ')[1].strip()
                        info_count += 1
                    if identifier == 'MSG':
                        conlon_index = 0
                        for char in line:
                            if char == ':':
                                break
                            else:
                                conlon_index += 1
                        for char in line[conlon_index+1: len(line)]:
                            tmp_msg += char
                        info_count += 1
                except:
                    print("[error] Config File Malformated. Trying Next Tag...")
                    inside_tag = False
                    info_count = 0


    msg_list.close()
    return send_content

def main():
    get = parse_file();
    print(get)


if __name__ == "__main__":
    main()
