import os
import json


def read_txt(file):
    with open(file) as f:
        rds = f.readlines()
        P2 = rds[2]
        P2 = P2.split(':')[1][1:]
        Tr_velo_to_cam = rds[5]
        Tr_velo_to_cam = Tr_velo_to_cam.split(':')[1][1:]

        P2 = [float(i) for i in P2.strip('\n').split(' ')]
        # print(P2)
        Tr_velo_to_cam = [float(i) for i in Tr_velo_to_cam.strip('\n').split(' ')]
        # print(Tr_velo_to_cam)

        return P2, Tr_velo_to_cam


def write_json(fx, fy, cx, cy, Tr_velo_to_cam, json_file):
    with open(template) as f:
        anno = json.load(f)
    # print(anno)
    print(anno['camera_0'])

    camera_internal = anno['camera_0']['camera_internal']
    camera_internal['fx'], camera_internal['fy'], camera_internal['cx'], camera_internal['cy'] = fx, fy, cx, cy
    # print(anno['camera_0'])

    anno['camera_0']['camera_external'] = Tr_velo_to_cam + [0, 0, 0, 1]
    # print(anno['camera_0'])

    anno_dict = {'camera_0': anno['camera_0']}
    print(anno_dict)

    js = open(json_file, 'w')
    js.write(json.dumps(anno_dict))
    js.close()


if __name__ == "__main__":

    calib_path = './calib'
    json_path = './json'
    template = 'camera-config.json'

    txt_file_list = os.listdir(calib_path)
    for txt_file in txt_file_list:
        print(txt_file)
        P2, Tr_velo_to_cam = read_txt(os.path.join(calib_path, txt_file))
        fu, fv, cu, cv = P2[0], P2[5], P2[2], P2[6]
        fx, fy, cx, cy = fu, fv, cu, cv
        # print(fx, fy, cx, cy)

        json_file = json_path + '/' + txt_file[:-4] + '.json'
        write_json(fx, fy, cx, cy, Tr_velo_to_cam, json_file)