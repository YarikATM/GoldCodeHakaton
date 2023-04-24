import csv
import datetime as dt
import cv2
from db import Database


db = Database('/Users/yaroslav/PycharmProjects/GoldCodeDjango/db.sqlite3')
start_time = dt.datetime(2023, 4, 22, 12, )


def get_data(path):
    lst_unload, lst_start_cord, lst_width_height, lst_time = [], [], [], []

    with open(path, newline='') as file:
        reader = csv.reader(file)

        for row in reader:
            lst_unload.append(row[1])

            start_x = int(row[2])
            start_y = int(row[3])

            end_x = int(row[4])
            end_y = int(row[5])

            lst_start_cord.append((start_x, start_y))
            lst_width_height.append((end_x, end_y))

            time = dt.datetime.strptime(row[6], '%H:%M:%S')
            seconds = time.second + time.minute * 60 + time.hour * 60 * 60

            lst_time.append(seconds)

    return lst_unload, lst_start_cord, lst_width_height, lst_time


def get_res_imgs(cap, lst_time, lst_start_cord, lst_width_height):
    cap.set(cv2.CAP_PROP_POS_MSEC, 68 * 1000)
    ret, first = cap.read()
    first = cv2.resize(first, (416, 416))

    for i in range(len(lst_time)):
        cap.set(cv2.CAP_PROP_POS_MSEC, lst_time[i] * 1000)
        ret, frame = cap.read()
        frame = cv2.resize(frame, (416, 416))
        res_frame = frame.copy()

        center_x = lst_start_cord[i][0]
        center_y = lst_start_cord[i][1]

        width = lst_width_height[i][0]
        height = lst_width_height[i][1]

        x_1 = center_x - width
        y_1 = center_y - height

        x_2 = center_x + width
        y_2 = center_y + height

        cv2.circle(first, (center_x, center_y), 4, (0, 0, 255), thickness=-1)

        cv2.rectangle(frame, (x_1, y_1), (x_2, y_2), (255, 0, 0), thickness=2)
        cv2.rectangle(frame, (100, 60), (220, 200), (0, 255, 0), thickness=2)

        title = f"img_{i + 1}_id_{lst_time[i]}_sec"

        if 100 <= center_x <= 210 and 60 <= center_y <= 200:

            cv2.circle(frame, (center_x, center_y), 3, (0, 255, 0), thickness=-1)

            cv2.imwrite(f'images/unload/{title}.jpg', frame)

            cv2.imwrite(f'/Users/yaroslav/PycharmProjects/GoldCodeDjango/GoldCode/static/GoldCode/img/{title}.jpg', res_frame)

            time = start_time + dt.timedelta(seconds=lst_time[i])

            img_path = f"images/{title}.jpg"

            if not db.shipment_exists(time, img_path):
                db.add_shipment(time, img_path)

            # Демонстрация результативных детектов
            # cv2.imshow('', frame)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

        else:
            cv2.circle(frame, (center_x, center_y), 3, (0, 0, 255), thickness=-1)

        cv2.imwrite('images/other/' + title + '.jpg', frame)

    cv2.imwrite(f'images/th.jpg', first)
        # Демонстрация всех детектов
        # cv2.imshow('', frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


def main():
    lst_unload, lst_start_cord, lst_width_height, lst_time = get_data('row_data/cora_transport_src_time.csv')

    cap = cv2.VideoCapture('row_data/front_loader_part_1.mp4')

    get_res_imgs(cap, lst_time, lst_start_cord, lst_width_height)


if __name__ == '__main__':
    main()
